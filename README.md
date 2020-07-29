# Pandemic
Pandemic is virus spread simulator.

## Install
```
cd padndemic
python3 -m pip install .
```

## Usage
Two versione cli and gui are available.
Both versions take as an argument a json file containing the parameters necessary to run the simulator.

The cli version also supports a folder as a parameter, a different instance of the simulator will be executed using each file individually as parameters.

### CLI

```
python3 -m pandemic.cli parameters.json
python3 -m pandemic.cli parameters_directory
```

### GUI

```
python3 -m pandemic.gui parameters.json
```

### Parameters
| Name                       | Type                   | Default   | Nullable | Description                                          |
|----------------------------|------------------------|-----------|----------|------------------------------------------------------|
| peers_number               | int                    | Mandatory | No       | number of peers                                      |
| hotspots_number            | int                    | Mandatory | No       | number of hotspots                                   |
| initial_infected_number    | int                    | Mandatory | No       | number of peers that are infected at the beginning   |
| patching_begin_epoch       | int                    | Mandatory | Yes      | number of the epoch from which peers can patch       |
| map_size                   | {x:int, y:int}         | Mandatory | No       | map size                                             |
| in_hotspots_probability    | float                  | Mandatory | No       | probability to generate a destination in a hotspot   |
| infection_probability      | float                  | Mandatory | No       | probability that a peer infects a peer in its radius |
| patch_probability          | float                  | Mandatory | No       | probability that a peer can be patched               |
| epoch_limit                | int                    | Mandatory | Yes      | number of the epoch in which the simulation ends     |
| peer_radius                | float                  | Mandatory | No       | radius of infectivity of a peer                      |
| hotspots_radius            | float                  | Mandatory | No       | radius indicating the size of the hotspot            |
| oss                        | [{os:str, prop:float}] | Mandatory | No       | operating systems and their distribution, the first defined is the one that will be infected |
| HtoH                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| HtoT                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| HtoE                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| TtoH                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| TtoT                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| TtoE                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| EtoH                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| EtoT                       | float                  | Mandatory | No       | mobility model probability of state changing         |
| EtoE1                      | float                  | Mandatory | No       | mobility model probability of state changing         |
| EtoE2                      | float                  | Mandatory | No       | mobility model probability of state changing         |
| exploringSpeedMax          | float                  | Mandatory | No       | maximum speed of a peer in E state                   |
| travelingSpeedMax          | float                  | Mandatory | No       | maximum speed of a peer in T state                   |
| acceleration               | float                  | Mandatory | No       | acceleration of a peer                               |
| output_directory           | str                    | null      | Yes      | name of the output directory                         |
| seed                       | int                    | null      | Yes      | if defined aa seed for randomness is setted          |
| zipf_alpha                 | float                  | 1.5       | No       | parameter of hotspot zipf distrinution               |
| zipf_range                 | int                    | 30        | No       | parameter of hotspot zipf distrinution               |
| width                      | int                    | 720       | No       | GUI parameter, width in pixel of the window          |
| ms                         | int                    | 16        | No       | GUI parameter, pause between epochs                  |

# PandemicAnalyzer
Analyzer of the pandemic output data.

## Install
```
cd padndemic_analyzer
python3 -m pip install .
```

## Usage
This program takes as argument or directly a result folder produced by pandemic or a folder containing more result folders produced by pandemic.
```
python3 -m pandemic_analyzer pandemic_result_directory
python3 -m pandemic-cli directory_containing_pandemic_result_directories
```
