# Frozen Emissions Change Log

* 2020-04-28
  * Shipping & aviation sectors removed from list of sectors to freeze (`emission_factor_file::_get_comb_factors()`).
    * 1A3ai_International-aviation
    * 1A3aii_Domestic-aviation
    * 1A3di_International-shipping
  * Reverted CEDS gridding seasonality mapping file added (`ceds_files/seasonality_mapping.csv`)