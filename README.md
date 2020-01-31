# Incident Counting Solution

Incident counting strategy: create dict with keys of incidents values and values, containing lists of time series
## Getting Started

To run project according to tests, we need to run docker container with last Anaconda and python3

### Prerequisites

To run you need installed docker.
```
install according your system
```

### Installing

Run this steps to perform incident counting on test file

```
git clone https://github.com/haimin777/incidCounter.git
cd incidCounter

```

Run docker anaconda in current directory

```
docker pull continuumio/anaconda3
docker run -v `pwd`:/home -it continuumio/anaconda3 /bin/bash
cd home/
python incident_finder.py -i input.csv -o output.csv -t 0.3
```

In result you can see execution time and output file in current directory


## Authors

* **Alex Haimin** 



