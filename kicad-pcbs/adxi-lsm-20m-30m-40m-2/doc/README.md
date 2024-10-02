# adxi-lsm-20m-30m-40m-2 Design documentation

This is the second attempt at designing a 'late stage module' for the [adxi project](https://github.com/vk2diy/adxi).

The primary difference with this revision is that, given the transistor had changed, recalculation was required.

Instead of fudging the use of external tools an attempt was made to build a for purpose tool, [classe2-calculator](https://github.com/vk2diy/classe2-calculator).

## 20m Design

```
$ ./classe2 -p 5 -v 12 -b 20m -t infinite --l1 7.755uh -m SI2304DDS -M pi

Input parameters:
 Output Power = 5W
 Supply Voltage = 12V
 MOSFET = SI2304DDS (Vdss=30V, Id=2.7A, Rds_on=0.049Ω, Ciss=235pF, Coss=45pF, Crss=17pF, Vgs_th=2.3375V)
 Q Factor = None

[20m] @ 14MHz-14.35MHz (c=14.175MHz, nbw=350kHz, bw=420kHz, q=33.75)
 Power Amplifier components:
  Topology = infinite
  L1 = 7.755µH (user-specified)
  L2 = 6.215µH
  C1 = 138.577pF
  C2 = 21.019pF
  R = 16.4Ω (before matching)

  Top 3 recommended Power Amplifier component configurations:

   Configuration 1: (0.02% error, estimated SRF margin 4.25 (Good), 6 parts)
     L2 = 6.2µH (1.5µH + 4.7µH) [ESR=2.00x] [I=0.50x]
     C1 = 140.426pF (150pF || 2.2nF) [ESR=0.50x] [I=2.00x]
     C2 = 21.016pF (22pF || 470pF) [ESR=0.50x] [I=2.00x]

   Configuration 2: (0.02% error, estimated SRF margin 4.25 (Good), 6 parts)
     L2 = 6.2µH (1.5µH + 4.7µH) [ESR=2.00x] [I=0.50x]
     C1 = 136.364pF (150pF || 1.5nF) [ESR=0.50x] [I=2.00x]
     C2 = 21.016pF (22pF || 470pF) [ESR=0.50x] [I=2.00x]

   Configuration 3: (0.02% error, estimated SRF margin 4.256 (Good), 6 parts)
     L2 = 6.182µH (6.8µH || 68µH) [ESR=0.50x] [I=2.00x]
     C1 = 140.426pF (150pF || 2.2nF) [ESR=0.50x] [I=2.00x]
     C2 = 21.016pF (22pF || 470pF) [ESR=0.50x] [I=2.00x]

 Matching Network Configurations:
  Configuration 1:
  C1_match: (0.00% error) 940pF (470pF + 470pF) [ESR=sum] [I=half]
  L_match: (0.00% error) 842nH (12nH + 150nH + 680nH) [ESR=sum] [I=smallest]
  C2_match: (0.00% error) 1.636nF (68pF + 68pF + 1.5nF) [ESR=sum] [I=smallest]

  Configuration 2:
  C1_match: (0.00% error) 940pF (470pF + 470pF) [ESR=sum] [I=half]
  L_match: (0.00% error) 842nH (12nH + 150nH + 680nH) [ESR=sum] [I=smallest]
  C2_match: (0.00% error) 1.633nF (33pF + 100pF + 1.5nF) [ESR=sum] [I=smallest]

  Configuration 3:
  C1_match: (0.00% error) 940pF (470pF + 470pF) [ESR=sum] [I=half]
  L_match: (0.00% error) 842nH (12nH + 150nH + 680nH) [ESR=sum] [I=smallest]
  C2_match: (0.01% error) 1.647nF (47pF + 100pF + 1.5nF) [ESR=sum] [I=smallest]


 Low Pass Filter Configurations:
  Configuration 1:
   C1_lpf: (0.00% error) 172.7pF (4.7pF + 68pF + 100pF) [ESR=sum] [I=smallest]
   L2_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C3_lpf: (0.00% error) 362pF (10pF + 22pF + 330pF) [ESR=sum] [I=smallest]
   L4_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C5_lpf: (0.00% error) 172.7pF (4.7pF + 68pF + 100pF) [ESR=sum] [I=smallest]

  Configuration 2:
   C1_lpf: (0.00% error) 172.7pF (4.7pF + 68pF + 100pF) [ESR=sum] [I=smallest]
   L2_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C3_lpf: (0.00% error) 362pF (10pF + 22pF + 330pF) [ESR=sum] [I=smallest]
   L4_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C5_lpf: (0.00% error) 173pF (1pF + 22pF + 150pF) [ESR=sum] [I=smallest]

  Configuration 3:
   C1_lpf: (0.00% error) 172.7pF (4.7pF + 68pF + 100pF) [ESR=sum] [I=smallest]
   L2_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C3_lpf: (0.00% error) 362pF (10pF + 22pF + 330pF) [ESR=sum] [I=smallest]
   L4_lpf: (0.00% error) 689nH (47nH + 82nH + 560nH) [ESR=sum] [I=smallest]
   C5_lpf: (0.00% error) 172pF (22pF + 150pF) [ESR=sum] [I=half]


                                                  ANTENNA
                                                  SYSTEM
                                                   |  |
======= Class E Power Amplifier ===================|==|===
                                                   |  |
   VCC--[L1]--[C1]--[C2]--[L2]--.       DRV--[MOSFET] |
               |                |               |     |
              GND               |              GND    |
                                |                     |
                                |                     |
 .------------------------------'                     |
 | Z<50Ω                                              |
=|===== Pi Matching Network ==========================|===
 |                                                    |
 `--[C1_match]--[L_match]--[C2_match]--.              |
       |                      |        |              |
      GND                    GND       |              |
                                       |              |
 .-------------------------------------'              |
 | Z=50Ω                                              |
=|===== Low Pass Filter ==============================|===
 |                                                    |
 `--[C1_lpf]--[L2_lpf]--[C3_lpf]--[L4_lpf]--[C5_lpf]--'
       |                   |                   |
      GND                 GND                 GND

==========================================================
```

PA configuration 1 was chosen, and was fairly straightforward to implement.

## 30m

```
./classe2 -p 5 -v 12 -b 30m -t infinite --l1 7.755uh -m SI2304DDS
Input parameters:
 Output Power = 5W
 Supply Voltage = 12V
 MOSFET = SI2304DDS (Vdss=30V, Id=2.7A, Rds_on=0.049Ω, Ciss=235pF, Coss=45pF, Crss=17pF, Vgs_th=2.3375V)
 Q Factor = None

[30m] @ 10.1MHz-10.15MHz (c=10.125MHz, nbw=50kHz, bw=60kHz, q=168.75)
 Topology = infinite
 L1 = 7.755µH (user-specified)
 L2 = 43.956µH
 C1 = 193.984pF
 C2 = 5.666pF
 R = 16.571Ω

Top 3 recommended component configurations:

  Configuration 1: (0.01% error, estimated SRF margin 2.234 (Concern), 6 parts)
  (SRF Concern: Consider using a different inductor or parallel combination for L2)
    L2 = 43.961µH (47µH || 680µH) [ESR=0.50x] [I=2.00x]
    C1 = 193.875pF (330pF || 470pF) [ESR=0.50x] [I=2.00x]
    C2 = 5.638pF (6.8pF || 33pF) [ESR=0.50x] [I=2.00x]

  Configuration 2: (0.01% error, estimated SRF margin 2.233 (Concern), 6 parts)
  (SRF Concern: Consider using a different inductor or parallel combination for L2)
    L2 = 44µH (22µH + 22µH) [ESR=2.00x] [I=0.50x]
    C1 = 193.875pF (330pF || 470pF) [ESR=0.50x] [I=2.00x]
    C2 = 5.638pF (6.8pF || 33pF) [ESR=0.50x] [I=2.00x]

  Configuration 3: (0.01% error, estimated SRF margin 2.234 (Concern), 6 parts)
  (SRF Concern: Consider using a different inductor or parallel combination for L2)
    L2 = 43.961µH (47µH || 680µH) [ESR=0.50x] [I=2.00x]
    C1 = 193.875pF (330pF || 470pF) [ESR=0.50x] [I=2.00x]
    C2 = 5.7pF (1pF + 4.7pF) [ESR=2.00x] [I=0.50x]
```

This was more difficult to implement.

Configuration 1 was chosen but there were no appropriate ways to obtain 47uH of inductance while maintaining a reasonable self-resonant frequency (SRF) - ie. ability to function at the required frequency level to be a useful resonator circuit.

It therefore took some time to find alternative topologies which were both current-capable and SRF-capable for this purpose, while maintaining a relatively low resistance.

## 40m

```
./classe2 -p 5 -v 12 -b 40m -t infinite --l1 7.755uh -m SI2304DDS
Input parameters:
 Output Power = 5W
 Supply Voltage = 12V
 MOSFET = SI2304DDS (Vdss=30V, Id=2.7A, Rds_on=0.049Ω, Ciss=235pF, Coss=45pF, Crss=17pF, Vgs_th=2.3375V)
 Q Factor = None

[40m] @ 7MHz-7.3MHz (c=7.15MHz, nbw=300kHz, bw=360kHz, q=19.861)
 Topology = infinite
 L1 = 7.755µH (user-specified)
 L2 = 7.18µH
 C1 = 300.553pF
 C2 = 73.35pF
 R = 16.242Ω

Top 3 recommended component configurations:

  Configuration 1: (0.01% error, estimated SRF margin 7.824 (Good), 6 parts)
    L2 = 7.19µH (390nH + 6.8µH) [ESR=2.00x] [I=0.50x]
    C1 = 300pF (330pF || 3.3nF) [ESR=0.50x] [I=2.00x]
    C2 = 72.7pF (4.7pF + 68pF) [ESR=2.00x] [I=0.50x]

  Configuration 2: (0.01% error, estimated SRF margin 7.824 (Good), 6 parts)
    L2 = 7.19µH (390nH + 6.8µH) [ESR=2.00x] [I=0.50x]
    C1 = 300pF (150pF + 150pF) [ESR=2.00x] [I=0.50x]
    C2 = 72.7pF (4.7pF + 68pF) [ESR=2.00x] [I=0.50x]

  Configuration 3: (0.01% error, estimated SRF margin 7.818 (Good), 6 parts)
    L2 = 7.2µH (12µH || 18µH) [ESR=0.50x] [I=2.00x]
    C1 = 300pF (330pF || 3.3nF) [ESR=0.50x] [I=2.00x]
    C2 = 72.7pF (4.7pF + 68pF) [ESR=2.00x] [I=0.50x]
```

Again, configuration 1 was chosen and the `L2` configuration proved the greatest challenge. Finally an approximation of 7.5uH rather than 7.2uH was chosen.

## Layout

With regards to the layout, some attempt was made to stagger inductors as they are supposed to be prone to magnetic coupling. Capacitors, not so much.
