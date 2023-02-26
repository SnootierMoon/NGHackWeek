# NGHackWeek

Our project for the 2022 Northrop Grumman Innovation Factory Hack Week @ UMD.

This program scrapes the web for products and their specs and enters them into
a database so that desired properties can be queried quickly.

## Usage:

This project depends on `aiohttp` for asynchronous HTTP, `BeautifulSoup` for
webscraping, and `tqdm` for some cool progress bars.

You can set up a development environment with a `venv` and then install the
required dependencies from `requirements.txt` asa follows:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

Then you will be able to run the program:

```sh
$ python3 main.py
```

The program will first prompt you for the product you are searching for. Type
in a product (e.g. `reaction wheel`), and then press enter. The program will
search the web for results.

```
Product Name: reaction wheel
found 6 pages, with 125 results
125 product urls retrieved
```

The program will then find spec categories associated with the product:

```
Fetched specs: 
  total_mass
  net_torque
  torque
  angular_speed_control_accuracy
  angular_momentum_storage
  speed_control_accuracy
  width
  magnetic_moment
  mechanical_vibration
  power_interface
  magnetic_gain
  moment_of_inertia
  ...
```

At this point, the program will ask you to enter SQL commands to view the data.
The program will tell you the name of the table in which the specs have been
stored. Each row of the table will have a field `Name` and a field for each
spec.

```
Use SQL commands in the table: product_specs
SQLite: SELECT Name,lifetime FROM product_specs WHERE lifetime IS NOT NULL;
  ('Reaction Wheel Assembly (RWA05-24)', '5 years LEO')
  ('Reaction Wheel Assembly (RWA-05)', '5 years LEO')
  ('RSI 18-220/45', '15 yr')
  ('Reaction Wheel RW-10NMS', '7 yr')
  ('Flywheel', '5 yr')
  ('RWP100 Reaction Wheel', '> 5 yr')
  ('RW 1 Type A', '1 year in low earth orbit')
  ('RWP500 Reaction Wheel', '> 10 yr')
  ('RSI 30-280/30', '> 15 yr')
  ('RWP015 Reaction Wheel', '> 5 yr')
  ('RWP050 Reaction Wheel', '> 5 yr')
  ('RW 1 Type B', '1 year in low earth orbit')
  ('MicroWheel 1000', '> 7 yr')
...
```
