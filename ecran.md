# Ecran

# Timestamp = Heure UTC

## Libray
```
$ curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
$ sudo bash rgb-matrix.sh
```

Modification du fichier 'samplebase.py' donné par la librairie
- Modification 1
```python
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=32, type=int)
```
```python
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=64, type=int)
```


- Modification 2
```python
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
```
```python
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=5, type=int)
```

## Exemple

```py
dataSimu=[
{'ligne': '05', 'terminus': 'Port de Commerce', 'temps': '1635365073.0'},
{'ligne': '05', 'terminus': 'Provence', 'temps': '1635367073.0'},
{'ligne': '01', 'terminus': 'Gare', 'temps': '1635367073.0'},
{'ligne': '01', 'terminus': 'Hôpital Cavale', 'temps': '1635367073.0'}
]
```
