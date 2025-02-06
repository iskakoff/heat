# Forced circulation heat transfer simulation

Project simulates heat transfer with forced circulation.

The following classes are defined:

- Pipe
    - defines simple pipe that can exchange energy with an environment
- Pump
    - defines the constant liquid flow rate
- Solar
    - describes liquid heating due to convection
- Tank
    - idealized storage tank that has no energy loss

To run simulation use `python main.py`. To adjust default parameters check available options with
`python main.py --help`.

## Known restriction:

- Only single pump is allowed
- Single pump is required
- Liquid flow in tank is assumed to be uniform in 1 direction