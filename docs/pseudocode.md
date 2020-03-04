# Psuedocode

### `driver::freeze_emissions()`
```
FOR species in emissions species to freeze:
  read the CMIP6 emissions factors file for the species;
  FOR sector in CEDS sectors:
    FOR fuel in CEDS fuels:
      IF the shape of the combustion sector dataframe != 0:
        calculate the median of the EF values for the sector & fuel combination at the EF freeze year;
        identify outliers in the EF values for the sector & fuel combination at the EF freeze year;
        IF the number of outliers identified is non-zero:
          set the outlying EF value(s) to the median EF value;
        END IF
      END IF
    END FOR
  END FOR
  set EF values for years >= 1971 to their 1970 value;
  inset the frozen combustion EFs into the master CMIP6 species EF dataframe;
  write species EF dataframe to csv;
END FOR
```


### `driver::calc_emissions()`
```
FOR species in emissions species to freeze:
  read the frozen emissions factors file for the species into dataframe;
  read the activity file for the species into dataframe;
  check that the two dataframes have identical column headers;
  multiply the EF and activity dataframes to compute total emissions;
  write the total emissions dataframe to csv;
END FOR
```
