// adxi-1.2 firmware
//
//  website: https://github.com/vk2diy/adxi
//  license: GPLv3 
//  credits: based on the ADX project @ https://github.com/WB2CBA/ADX
//
//  major changes from ADX-era firmware:
//   - restructured for platformio
//   - restructured for adxi-1.2 hardware
//   - removed blinkenlights / buttons interface
//   - removed EEPROM use

// libraries
#include <si5351.h>     // clock generator
#include "Wire.h"       // I2C

// MCU pin definitions
#define PIN_CM108B_LEDR_INPUT 2
#define PIN_CM108B_LEDO_INPUT 3
#define PIN_TUSB321_IMODE1_INPUT 4
#define PIN_TUSB321_IMODE2_INPUT 5
#define PIN_HOST_FSK_INPUT 7
#define PIN_RECEIVE_ENABLE_WHEN_LOW_OUTPUT 8
#define PIN_PA_DRIVE_PWM_OUTPUT 9
#define PIN_SPI_MOSI 11
#define PIN_SPI_SS_3V3OUTPUTS 12
#define PIN_SPI_SCK 13
#define PIN_FORWARD_POWER_INPUT 14
#define PIN_REVERSE_POWER_INPUT 15
#define PIN_I2C_SDA 18
#define PIN_I2C_SCL 19

// 3.3V output pin definitions
#define PIN_3V3OUT_CM108B_VOLUME_UP_WHEN_LOW 1
#define PIN_3V3OUT_CM108B_VOLUME_DOWN_WHEN_LOW 2
#define PIN_3V3OUT_CM108B_MUTE_RECORDING_WHEN_LOW 3
#define PIN_3V3OUT_CM108B_MUTE_PLAYBACK_WHEN_LOW 4
#define PIN_3V3OUT_CM108B_SLEEP_WHEN_LOW 5

// other
#define SI5351_REF 25000000UL // 25MHz

// constants
unsigned long SI5351_CALIBRATION_FREQUENCY_HZ = 1000000UL; // 1MHz = 1000000Hz
unsigned long SI5351_CALIBRATION_FACTOR = 0;

// ---------------- unsorted prior variable definitions: not yet reviewed ----------------
unsigned int temp = 0;
unsigned int mode = 0;
unsigned int Band_slot = 0;
unsigned int Band = 0;

boolean TX_State = 0;

unsigned long freq = 0;
unsigned long F_FT8;
unsigned long F_FT4;
unsigned long F_JS8;
unsigned long F_WSPR;

boolean cat_stat = 0;
boolean TxStatus = 0; //0 =  RX 1=TX
unsigned int CAT_mode = 2;
String received;
String receivedPart1;
String receivedPart2;
String command;
String command2;
String parameter;
String parameter2;
String sent;
String sent2;

//**********************************[ BAND SELECT ]************************************************
// ADX can support up to 4 bands on board. Those 4 bands needs to be assigned to Band1 ... Band4 from supported 6 bands.
// To change bands press SW1 and SW2 simultaneously. Band LED will flash 3 times briefly and stay lit for the stored band. also TX LED will be lit to indicate
// that Band select mode is active. Now change band bank by pressing SW1(<---) or SW2(--->). When desired band bank is selected press TX button briefly to exit band select mode.
// Now the new selected band bank will flash 3 times and then stored mode LED will be lit.
// TX won't activate when changing bands so don't worry on pressing TX button when changing bands in band mode.

// Assign your prefered bands to B1,B2,B3 and B4
// Supported Bands are: 80m, 40m, 30m, 20m,17m, 15m

unsigned int Band1 = 40; // Band 1 // These are my default bands. Feel free to swap with yours
unsigned int Band2 = 30; // Band 2
unsigned int Band3 = 20; // Band 3
unsigned int Band4 = 17; // Band 4

Si5351 si5351;

//*************************************[ SETUP FUNCTION ]**************************************
void setup() {
  pinMode(PIN_CM108B_LEDR_INPUT,INPUT);
  pinMode(PIN_CM108B_LEDO_INPUT,INPUT);
  pinMode(PIN_TUSB321_IMODE1_INPUT,INPUT);
  pinMode(PIN_TUSB321_IMODE2_INPUT,INPUT);
  pinMode(PIN_HOST_FSK_INPUT,INPUT);
  pinMode(PIN_RECEIVE_ENABLE_WHEN_LOW_OUTPUT,OUTPUT);
  pinMode(PIN_PA_DRIVE_PWM_OUTPUT,OUTPUT);
  pinMode(PIN_SPI_MOSI,OUTPUT);
  pinMode(PIN_SPI_SS_3V3OUTPUTS,OUTPUT);
  pinMode(PIN_SPI_SCK,OUTPUT);
  pinMode(PIN_FORWARD_POWER_INPUT,INPUT);
  pinMode(PIN_REVERSE_POWER_INPUT,INPUT);
  pinMode(PIN_I2C_SDA,INPUT);
  pinMode(PIN_I2C_SCL,OUTPUT);

  digitalWrite(PIN_RECEIVE_ENABLE_WHEN_LOW_OUTPUT,HIGH);
  digitalWrite(PIN_PA_DRIVE_PWM_OUTPUT,LOW);
  digitalWrite(PIN_SPI_MOSI,LOW);
  digitalWrite(PIN_SPI_SS_3V3OUTPUTS,LOW);
  digitalWrite(PIN_SPI_SCK,LOW);
  digitalWrite(PIN_I2C_SCL,LOW);

  Serial.begin(115200);
  //Serial.setTimeout(4);

  Serial.println(F("adxi-1.2"));
  Serial.println(F(" "));
  Serial.println(F("init"));
  
  Serial.print(F(" - "));
  Serial.print(F("si5351"));
  Serial.print(F("..."));
  Serial.print(F(" "));
  si5351.init(SI5351_CRYSTAL_LOAD_10PF, 0, 0); // Ooh dang! We have 12pF. That's not good. Bug!
  si5351.set_correction(SI5351_CALIBRATION_FACTOR, SI5351_PLL_INPUT_XO);
  si5351.set_pll(SI5351_PLL_FIXED, SI5351_PLLA);
  si5351.drive_strength(SI5351_CLK0, SI5351_DRIVE_8MA); // maximum power on transmit clock
  si5351.drive_strength(SI5351_CLK1, SI5351_DRIVE_2MA); // reduced power on receive clock
  si5351.drive_strength(SI5351_CLK2, SI5351_DRIVE_2MA); // unused
  si5351.set_clock_pwr(SI5351_CLK0, 0); // disable at startup
  si5351.set_clock_pwr(SI5351_CLK1, 0); // disable at startup
  si5351.set_clock_pwr(SI5351_CLK2, 0); // unused
  Serial.println(F("ok"));

  Serial.print(F(" - "));
  Serial.print(F("timer"));
  Serial.print(F("..."));
  Serial.print(F(" "));
  TCCR1A = 0x00;
  TCCR1B = 0x01; // Timer1 Timer 16 MHz
  TCCR1B = 0x81; // Timer1 Input Capture Noise Canceller
  Serial.println(F("ok"));

  Serial.print(F(" - "));
  Serial.print(F("comparator"));
  Serial.print(F("..."));
  Serial.print(F(" "));
  ACSR |= (1<<ACIC);  // Analog Comparator Capture Input
  Serial.println(F("ok"));

}

void receive_enable() {
 si5351.output_enable(SI5351_CLK0, 0); // transmit disable
 si5351.set_freq(freq * 100ULL, SI5351_CLK1); // set receive frequency
 si5351.output_enable(SI5351_CLK1, 1); // receive enable
}

void transmit_enable() {
 si5351.output_enable(SI5351_CLK1, 0); // receive disable
 si5351.output_enable(SI5351_CLK0, 1); // transmit enable
}

unsigned int get_forward_power(void) {
 return analogRead(PIN_FORWARD_POWER_INPUT);
}

unsigned int get_reverse_power(void) {
 return analogRead(PIN_REVERSE_POWER_INPUT);
}

unsigned int get_standing_wave_ratio(void) {
 unsigned int rvp;
 unsigned int fwp;
 rvp = get_reverse_power();
 if(rvp!=0) {
  fwp = get_forward_power();
  return fwp/rvp;
 }
 return 0;
}

void loop() {

  unsigned int fwp;
  fwp = get_forward_power();
  unsigned int rvp;
  rvp = get_reverse_power();
  unsigned int swr;
  swr = get_standing_wave_ratio();

  // print status information
  Serial.print(F(" - "));
  Serial.print(F("FWP"));
  Serial.print(F(": "));
  Serial.print(fwp);
  Serial.print(F(" / "));
  Serial.print(F("RVP"));
  Serial.print(F(": "));
  Serial.print(rvp);
  Serial.print(F(" / "));
  Serial.print(F("SWR"));
  Serial.print(F(": "));
  Serial.println(swr);

  delay(200);
  // simply print what is received
//  if(Serial.available()>0) {
//   Serial.print(Serial.readString());
//  }

/*
  if ((Serial.available() > 0) || (cat_stat == 1)) {
    Serial.print(F("_"));
    cat_stat = 1;
    process_host_serial_input();
    receive_enable();
  }
  else {  
    Serial.print(F("*"));

   // The following code is from JE1RAV https://github.com/je1rav/QP-7C
   //(Using 3 cycles for timer sampling to improve the precision of frequency measurements)
   //(Against overflow in low frequency measurements)
 
   int FSK = 1;
   int FSKtx = 0;
 
   while (FSK>0) {
     int Nsignal = 10;
     int Ncycle01 = 0;
     int Ncycle12 = 0;
     int Ncycle23 = 0;
     int Ncycle34 = 0;
     unsigned int d1=1,d2=2,d3=3,d4=4;
 
     TCNT1 = 0;
     while (ACSR &(1<<ACO)) {
       if (TIFR1&(1<<TOV1)) {
         Nsignal--;
         TIFR1 = _BV(TOV1);
         if (Nsignal <= 0) {
           break;
         }
       }
     }
     while ((ACSR &(1<<ACO))==0) {
       if (TIFR1&(1<<TOV1)) {
         Nsignal--;
         TIFR1 = _BV(TOV1);
         if (Nsignal <= 0) {
           break;
         }
       }
     }
     if (Nsignal <= 0) {
       break;
     }
     TCNT1 = 0;
     while (ACSR &(1<<ACO)) {
         if (TIFR1&(1<<TOV1)) {
         Ncycle01++;
         TIFR1 = _BV(TOV1);
         if (Ncycle01 >= 2) {
           break;
         }
       }
     }
     d1 = ICR1;
     while ((ACSR &(1<<ACO))==0) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle12++;
         TIFR1 = _BV(TOV1);
         if (Ncycle12 >= 3) {
           break;
         }
       }
     }
     while (ACSR &(1<<ACO)) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle12++;
         TIFR1 = _BV(TOV1);
         if (Ncycle12 >= 6) {
           break;
         }
       }
     }
     d2 = ICR1;
     while ((ACSR &(1<<ACO))==0) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle23++;
         TIFR1 = _BV(TOV1);
         if (Ncycle23 >= 3) {
           break;
         }
       }
     }
     while (ACSR &(1<<ACO)) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle23++;
         TIFR1 = _BV(TOV1);
         if (Ncycle23 >= 6) {
           break;
         }
       }
     }
     d3 = ICR1;
     while ((ACSR &(1<<ACO))==0) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle34++;
         TIFR1 = _BV(TOV1);
         if (Ncycle34 >= 3) {
           break;
         }
       }
     }
     while (ACSR &(1<<ACO)) {
       if (TIFR1&(1<<TOV1)) {
         Ncycle34++;
         TIFR1 = _BV(TOV1);
         if (Ncycle34 >= 6) {
           break;
         }
       }
     }
     d4 = ICR1;
     unsigned long codefreq1 = 1600000000/(65536*Ncycle12+d2-d1);
     unsigned long codefreq2 = 1600000000/(65536*Ncycle23+d3-d2);
     unsigned long codefreq3 = 1600000000/(65536*Ncycle34+d4-d3);
     unsigned long codefreq = (codefreq1 + codefreq2 + codefreq3)/3;
     if (d3==d4) codefreq = 5000;
     if ((codefreq < 310000) && (codefreq >= 10000)) {   // Frequency between 100 Hz and 3100 Hz
       if (FSKtx == 0) { transmit_enable(); }
       // update transmit clock frequency
       si5351.set_freq((freq * 100ULL + codefreq), SI5351_CLK0);
       if (cat_stat == 1) process_host_serial_input();
       FSKtx = 1;
     }
     else {
       FSK--;
     }
   }
 
   receive_enable();
   TX_State = 0;
   FSKtx = 0;
 }
 */
}

// void band_frequencies(void) {
//   switch (Band) {
//     case 80:
//       F_FT8 = 3573000;
//       F_FT4 = 3575000;
//       F_JS8 = 3578000;
//       F_WSPR = 3568600;
//       break;
//     case 40:
//       F_FT8 = 7074000;
//       F_FT4 = 7047500;
//       F_JS8 = 7078000;
//       F_WSPR = 7038600;
//       break;
//     case 30:
//       F_FT8 = 10136000;
//       F_FT4 = 10140000;
//       F_JS8 = 10130000;
//       F_WSPR = 10138700;
//       break;
//     case 20:
//       F_FT8 = 14074000;
//       F_FT4 = 14080000;
//       F_JS8 = 14078000;
//       F_WSPR = 14095600;
//       break;
//     case 17:
//       F_FT8 = 18100000;
//       F_FT4 = 18104000;
//       F_JS8 = 18104000;
//       F_WSPR = 18104600;
//       break;
//     case 15:
//       F_FT8 = 21074000;
//       F_FT4 = 21140000;
//       F_JS8 = 21078000;
//       F_WSPR = 21094600;
//       break;
//     case 10:
//       F_FT8 = 28074000;
//       F_FT4 = 28180000;
//       F_JS8 = 28078000;
//       F_WSPR = 28124600;
//       break;
//   }
// }

// void SI5351_VFO_calibration(){
//   // Set CLK2 output
//   //si5351.set_correction(SI5351_CALIBRATION_FACTOR, SI5351_PLL_INPUT_XO);
//   si5351.set_freq(SI5351_CALIBRATION_FREQUENCY_HZ * 100ULL, SI5351_CLK2);
//   si5351.drive_strength(SI5351_CLK2, SI5351_DRIVE_2MA); // low power
//   si5351.set_clock_pwr(SI5351_CLK2, 1); // enable clock
//   delay(100); // FIXTHIS: avoid delay()
//   si5351.set_clock_pwr(SI5351_CLK2, 0); // disable clock
// }

// this whole function needs rewriting and can probably be made substantially more efficient
//  ideas:
//   - accept only capitalized input
//   - parse character by character instead of converting to lines in multiple passes then pulling substrings
void process_host_serial_input(void) {

  received = Serial.readString();
  received.toUpperCase(); // this is a performance loss
  received.replace("\n",""); // this is a performance loss

  String data = "";
  int bufferIndex = 0;

  for (unsigned int i = 0; i < received.length(); ++i) {
    char c = received[i];
    if (c != ';') {
      data += c;
    }
    else {
      if (bufferIndex == 0) {
        data += '\0';
        receivedPart1 = data;
        bufferIndex++;
        data = "";
      }
      else {
        data += '\0';
        receivedPart2 = data;
        bufferIndex++;
        data = "";
      }
    }
  }

  command = receivedPart1.substring(0,2);
  command2 = receivedPart2.substring(0,2);
  parameter = receivedPart1.substring(2,receivedPart1.length());
  parameter2 = receivedPart2.substring(2,receivedPart2.length());

  if (command == "FA") {
    if (parameter != "") {
      freq = parameter.toInt();
      //VfoRx = VfoTx;
    }
    sent = "FA" // Return 11 digit frequency in Hz.
      + String("00000000000").substring(0,11-(String(freq).length()))
      + String(freq) + ";";
  }
  else if (command == "PS") {
    sent = "PS1;";
  }
  else if (command == "TX") {
    sent = "TX0;";
    transmit_enable();
    TxStatus = 1;
  }
  else if (command == "RX") {
    sent = "RX0;";
    receive_enable();
    TxStatus = 0;
  }
  else  if (command == "ID") {
    sent = "ID019;";
  }
  else if (command == "AI") {
    sent = "AI0;";
  }
  else if (command == "IF") {
    if (TxStatus == 1) {
      sent = "IF" // Return 11 digit frequency in Hz.
        + String("00000000000").substring(0,11-(String(freq).length()))
        + String(freq) + "00000" + "+" + "0000" + "0" + "0" + "0" + "00" + "1" + String(CAT_mode) + "0" + "0" + "0" + "0" + "000" + ";";
    }
    else {
      sent = "IF" // Return 11 digit frequency in Hz.
        + String("00000000000").substring(0,11-(String(freq).length()))
        + String(freq) + "00000" + "+" + "0000" + "0" + "0" + "0" + "00" + "0" + String(CAT_mode) + "0" + "0" + "0" + "0" + "000" + ";";
    }
  }
  else if (command == "MD") {
    sent = "MD2;";
  }

  //------------------------------------------------------------------------------

  if (command2 == "ID") {
    sent2 = "ID019;";
  }

  if (bufferIndex == 2) {
    Serial.print(sent2);
  }
  else {
    Serial.print(sent);
  }

  if ((command == "RX") || (command = "TX")) delay(50); // FIXTHIS: avoid delay()
  sent = String("");
  sent2 = String("");
}
