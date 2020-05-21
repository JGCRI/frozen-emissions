# ------------------------------------------------------------------------------
# Program Name: CEDS_version_comparison.R
# Author: Patrick O'Rourke
# Date Last Updated: April 10, 2020
# Program Purpose: Produces comparison-diagnostic files and plots between CEDS versions.
#                  Comparison by region and aggregate sectors as well as global totals.
# Input Files: RCP Region Mapping.xlsx, RCP_CEDS_sector_map.csv,
#                 Master_Sector_Level_map.csv, Master_Country_List.csv,
#                 CEDS_[em]_emissions_by_country_CEDS_sector_[YYYY_MM_DD].csv, CEDS_[em]_global_emissions_by_fuel_.csv (if comparing to previous run)
#                 [em]_CEDS_emissions_by_sector_country_v2016_07_26.csv (if comparing to CMIP paper),
#                 [em]_CEDS_emissions_by_sector_country_v2017_05_18.csv (if comparing to CO2 or CH4 to CMIP paper( v2016_07_26 for all other ems ) ),
#                 CH4_Extension_CEDS_emissions_by_sector_region_v2017_05_18.csv (if comparing CH4 to  CMIP paper( v2016_07_26 for all other ems ) )
# Output Files: CEDS_version_comparison-Select_CMIP_regions-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-CMIP_regions-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-Global_by_CMIP_sectors-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-Global_by_CMIP_sectors-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-Global_total-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-Global_total-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-Global_total_by_fuel-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-Global_total_by_fuel-[CEDS_start_year]_[CEDS_end_year].xlsx
#               CEDS_version_comparison-Africa_by_sec-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-Africa_by_sec-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-ROW_by_sec-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-ROW_by_sec-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-[reg1]_by_sec-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-[reg1]_by_sec-[CEDS_start_year]_[CEDS_end_year].xlsx,
#               CEDS_version_comparison-[reg2]_by_sec-[CEDS_start_year]_[CEDS_end_year].pdf,
#               CEDS_version_comparison-[reg2]_by_sec-[CEDS_start_year]_[CEDS_end_year].xlsx
# Note(s):
#       1) This script is designed to run from CEDS_Data, with CEDS_Data and CEDS on the same directory level
#          (example: desktop/CEDS and desktop/CEDS_Data). The CEDS repository is also assumed to be named "CEDS",
#          not "CEDS-dev". If you're repository is named "CEDS-dev", then it will either need to be renamed or
#          the references to "CEDS" in directory paths below will need to be modified to "CEDS-dev".
#
#       2) If you are comparing a previous run vs. a current run, both sets of final emissions must be in their respective
#          CEDS directories (CEDS/final-emissions/current-versions and CEDS/final-emissions/previous-versions)
#          If you are comparing a current run to a CEDS release, then the CEDS release final emissions need to be
#          within the release's emissions archive directory of CEDS_Data (example: for the CEDS CMIP release,
#          this directory would be the CEDS_Data/emission-archives/v2016_07_26)
#
#       3) There are many options for the user found in section 0.5 of this script. They include:
#          - Defining what type of previous run your are comparing to (a release, or the previous run in the CEDS directory).
#          - Defining the version tag of the current CEDS run
#          - Defining what final emission species you would like to compare. Configured by default to compare
#            all CEDS emission species.
#          - Years to compare (start year, end year, and a seperate CH4 start year if desired)
#          - Sectors to not include in the comparison, for both CEDS versions (by default agricultural waste burning,
#            other not in total, volcanoes, forest fires, and other natural emissions are omitted).
#          - Regions to not include in the comparison, for both CEDS versions (set to NULL by default)
#          - 5 regions to compare - these must be RCP regions
#          - A maximum of 2 user selected regions to graph by sector if desired - these must be RCP regions.
#            If 1 or 2 regions are defined, then two additional regions are graphed by sector:
#            1) Africa - an aggregate region containing all African RCP regions.
#            2) Rest of World - all regions not in the African aggregrate region and not
#               defined selected by the user to graph by region and sector.
#            Note that if the user selects and RCP African region to graph, they will still also be
#            included in the African aggregate region.
#          - Whether or not you desire titles at the top of the graphs
#
# TODO: (1) Address TODOs within this script,
#       (2) Functionalize script and move functions to a function only script
#       (3) Use something other than a loop
# ---------------------------------------------------------------------------

# 0. Read in global settings and headers

# Define a single CEDS_ROOT directory to make modification easier.
CEDS_ROOT <- "CEDS-frozen-emissions"
CEDS_DATA_ROOT <- "CEDS_Data-frozen_emissions"

# Define PARAM_DIR as the location of the CEDS "parameters" directory, relative
# to the "input" directory.
PARAM_DIR <- paste0("../", CEDS_ROOT, "/code/parameters/")

# Call standard script header function to read in universal header files -
# provide logging, file support, and system functions - and start the script log.
headers <- c( "data_functions.R", "analysis_functions.R",'process_db_functions.R',
              'common_data.R', 'IO_functions.R', 'data_functions.R', 'timeframe_functions.R') # Additional function files may be required.
log_msg <- "Print paper figures for detailed comparisons to previous CEDS version." # First message to be printed to the log
script_name <- "CEDS_version_comparison.R"

source( paste0( PARAM_DIR, "header.R" ) )

# Redfine PARAM_DIR as sourcing header.R sets PARAM_DIR to "../code/parameters/"
# and getwd() currently returns CEDS_Data/input
PARAM_DIR <- paste0("../../", CEDS_ROOT, "/code/parameters/")
initialize( script_name, log_msg, headers )

# TODO: We may want to remove the use of scales in the system unless version controlled (we probably shouldn't explicitly load packages in scripts).
library( 'scales' ) # Needed for regional plot, "comma" call

# ---------------------------------------------------------------------------
# 0.5. Script Options

# Previous CEDS version to compare to. Notes:
#   1) If you are running against the previous CEDS run (final-emissions/previous-versions),
#      set the previous_CEDS_version parameter to NULL.
#   2) If you are running against a previous CEDS release, then assign previous_CEDS_version
#      parameter to the version tag of the release (everything at the end of the final emissions
#      file name:
#      Current CEDS release versions include:
#      A) "v2016_07_26"    ---   Release 1 - CMIP release (first emissions release)
#      B) "v_2019_12_23"   ---   Release 2 - 1st official CEDS data system release
  previous_CEDS_version <- "v_07_26_2016"

# Current CEDS version to use. Notes:
# 1) Insert the version tag below (everything at the end of the final emissions file name,
#    or "v_YYYY_MM_DD" since the CMIP release)
# 2) This script is not configured to allow for CMIP release formatted final emissions
#    to run as a "current" version of CEDS. CMIP release formatted files canonly be used as
#    the "previous" version currently.
  current_CEDS_version <- "v_2020_1_13"

# Emissions species to compare.
# Note: If you decide not to compare all CEDS emission species, then Section 11 of this script
#       will need to be modified. For more details, please see Section 11.
  # em_list <- c( "BC", "CH4", "CO", "CO2", "NH3", "NMVOC", "NOx", "OC", "SO2" )

  # Remove CH4 and CO2 since frozen emissions weren't produced for these species.
  em_list <- c( "BC", "CO", "NH3", "NMVOC", "NOx", "OC", "SO2" )

# Years to compare - to change, redefine CEDS_start_year and CEDS_end_year.
# Note: These must be years that are available in the current_CEDS_version.
#       It is ok if the previous version being compared to has an earlier end year
#       than what is defined below, as the code will automatically account for that.
  CEDS_start_year <- 1960 # If set to historical_pre_extension_year, this is Currently: 1750
  CEDS_end_year <- end_year # If set to end_year, this is currently: 2014
  X_all_CEDS_years <- paste0( "X", CEDS_start_year : CEDS_end_year )
  CH4_start_year <- 1970 # Note: Set to NULL if CH4 can have the same years as other ems.

# Sectors to not compare
  current_CEDS_version_sectors_to_remove <- c(  "3F_Agricultural-residue-burning-on-fields", "6B_Other-not-in-total",
                                                "11A_Volcanoes", "11B_Forest-fires",  "11C_Other-natural" )

  printLog( paste0( "The following sector(s) from the current CEDS version ",
                    "will not be included in the comparison: " ), current_CEDS_version_sectors_to_remove )

  previous_CEDS_version_sectors_to_remove <- current_CEDS_version_sectors_to_remove

  printLog( paste0( "The following sector(s) from the previous CEDS version ",
                    "will not be included in the comparison: " ), previous_CEDS_version_sectors_to_remove )

# Regions to not compare
  current_CEDS_version_regions_remove <- c(  )

  if( !is.null( current_CEDS_version_regions_remove ) ){

    printLog( paste0( "The following region(s) from the current CEDS version ",
                      "will not be included in the comparison: "), current_CEDS_version_regions_remove )

  }

  previous_CEDS_version_regions_remove <- current_CEDS_version_regions_remove

  if( !is.null( previous_CEDS_version_regions_remove ) ){

    printLog( paste0( "The following region(s) from the previous CEDS version ",
                      "will not be included in the comparison: "), previous_CEDS_version_regions_remove )

  }

# 5 Regions to compare
# Note: These must be RCP regions. See complete_region_map object below,
#       column "Region" for available regions.
  regions_to_compare <- c( "China+", "India", "Russia+", "USA", "Western Africa" )

# Define regions for regional by sector comparisons
# Note: These must be RCP regions. See complete_region_map object below,
#       column "Region" for available regions.
#       This cannot contain more than 2 regions at present.
  RCP_regions_for_reg_by_sec_comparison <- c( "China+", "India" ) # Set to NULL if you don't want to produce these graphs

# Add titles to graphs? Notes:
#   Set to F if using the Rmarkdown, as the pdf pages will have graph titles already.
#   Set to T if not using the Rmarkdown
  include_titles_on_graphs <- T

# ---------------------------------------------------------------------------
# 1. Load and process mapping files, define script functions

# Master coutry list - mapping file
  setwd( paste0("../../", CEDS_ROOT, "/input") )

# Comparison mapping files
  MSL_map <-   Map_region_codes <- readData( "MAPPINGS", "Master_Sector_Level_map", meta = FALSE )
  MCL <- readData( domain = 'MAPPINGS', file_name = 'Master_Country_List' )

  Map_region_codes <- readData( "EM_INV", domain_extension = 'RCP/',"RCP Region Mapping", ".xlsx", sheet_selection = 'Reg Codes',
                                meta = FALSE )
  Map_iso_codes <- readData( "EM_INV", domain_extension = 'RCP/',"RCP Region Mapping", ".xlsx", sheet_selection = 'EDGAR32 & IEA',
                             meta = FALSE )
  Map_sector <- readData( "EM_INV", domain_extension = 'RCP/',"RCP_CEDS_sector_map",
                          meta = FALSE )

# Create complete region map for CEDS to RCP
  complete_region_map <- merge( Map_iso_codes, Map_region_codes,
                                by.x= "RCP Template Reg #",
                                by.y=, 'RCP Template Reg Code' )
  complete_region_map$Region <- gsub( " [(]Rest of[)]","",complete_region_map$Region )
  complete_region_map$Region <- gsub( " [(]Estonia, Latvia, Lithuania[)]","",complete_region_map$Region )
  complete_region_map$Region <- gsub( " [(]Republic of Korea[)]","", complete_region_map$Region )
  complete_region_map$Region <- gsub( " [(]Democratic People's Republic of Korea[)]","", complete_region_map$Region )
  complete_region_map[ which( complete_region_map$Code == 'GRL' ),'Region' ] <- 'Greenland'
  complete_region_map$Region <- gsub( " $","", complete_region_map$Region, perl = T )
  complete_region_map <- dplyr::mutate( complete_region_map, Code = tolower( Code ) )

#   Check if all isos listed in RCP region map are within the MCL, and
#   that all isos in the MCL are within the RCP region map
# TODO: Change this to the updated iso_check function once available (iso_check in analysis_functions.R)
  MCL_clean <- MCL %>%
    dplyr::select( iso, final_data_flag ) %>%
    dplyr::distinct( ) %>%
    dplyr::filter( final_data_flag == 1 | iso %in% c( "srb (kosovo)", "gum" ) ) %>%
    dplyr::filter( iso != "global" ) %>%
    dplyr::select( -final_data_flag )

  unique_RCP_map_isos <- sort( unique( complete_region_map$Code ) )
  unique_MCL_isos <- sort( unique( MCL_clean$iso ) )

#   A.) Check if all isos listed in RCP region map are within the MCL
    RCP_map_isos_not_in_MCL <- subset( unique_RCP_map_isos,
                                       !( unique_RCP_map_isos %in% unique_MCL_isos ) )

    if( length( RCP_map_isos_not_in_MCL ) != 0 ){

      printLog( RCP_map_isos_not_in_MCL )

      warning( paste0( "The above isos are in the RCP region mapping file but not ",
                       "final CEDS isos in Master_Country_List.csv... " ) )

    } else {

      printLog( "All isos in the in the RCP region mapping are",
                "final CEDS isos in Master_Country_List.csv..." )

    }

#   B.) Check if all isos in MCL (with final_data_flag of 1, srb(kosovo), and gum)
#   Are within the GAINS region mapping file
    MCL_isos_not_in_RCP_map <- subset( unique_MCL_isos,
                                       !( unique_MCL_isos %in% unique_RCP_map_isos ) )

    if( length( MCL_isos_not_in_RCP_map ) != 0 ){

      printLog( MCL_isos_not_in_RCP_map )

      stop( paste0( "The above isos are final CEDS isos in Master_Country_List.csv ",
                    "but not found in the RCP region mapping file...") )

    } else {

      printLog( "All final CEDS isos in Master_Country_List.csv are within",
                "the RCP region mapping file...")

    }

# Create sector map (fix mapping for international bunkers and fossil fuel fires)
  international_shipping_sectors <- c( "1A3di_Oil_tanker_loading", "1A3di_Oil_Tanker_Loading",
                                       "1A3di_International-shipping" )

  aviation_sectors <- c( "1A3ai_International-aviation", "1A3aii_Domestic-aviation" )

  tanker_map_rows <- Map_sector %>%
    dplyr::slice( 1 : 2 ) %>%
    dplyr::mutate( CEDS = c( "1A3di_Oil_tanker_loading", "1A3di_Oil_Tanker_Loading" ) )

  sector_map <- Map_sector %>%
    dplyr::bind_rows( tanker_map_rows ) %>%
    dplyr::mutate( RCP = if_else( CEDS %in% aviation_sectors, "AVIATION",
                                  if_else( CEDS %in% international_shipping_sectors, "INT. SHIPPING",
                                  if_else( RCP == "AWB", NA_character_, RCP ) ) ) ) %>%
    dplyr::mutate( RCP = if_else( CEDS == "7A_Fossil-fuel-fires", "ENE", RCP ) ) %>% # Fixing this here, as mapping file
                                                                                     # is used for other comparisons which don't
                                                                                     # include Fossil Fuel Fires
    dplyr::rename( sector = CEDS )

#   Check if CEDS sectors are present in the sector map, and that all CEDs sectors listed in the map
#   are CEDS sectors
#   TODO: Change this to the updated check function once available (iso_check in analysis_functions.R ionce
#   it can be used for sectors as well
  unique_RCP_map_CEDS_sectors <- sort( unique( sector_map$sector ) )
  unique_MSL_CEDS_sectors <- sort( unique( MSL_map$working_sectors_v1 ) )

#   A.) Check if all CEDS sectors listed in the RCP region map are within the MSL
    RCP_map_CEDS_sectors_not_in_MSL <- subset( unique_RCP_map_CEDS_sectors,
                                               !( unique_RCP_map_CEDS_sectors %in% unique_MSL_CEDS_sectors ) )

    if( length( RCP_map_CEDS_sectors_not_in_MSL ) > 1 |
        length( RCP_map_CEDS_sectors_not_in_MSL ) == 1 &  RCP_map_CEDS_sectors_not_in_MSL[1] !=  "1A3di_Oil_tanker_loading"){

      printLog( RCP_map_CEDS_sectors_not_in_MSL )

      stop( paste0( "The above sectors are in the RCP sector mapping file but not ",
                    "CEDS sectors in the Master_Sector_Level_map.csv... " ) )

    } else {

      printLog( "All sectors in the in the RCP sector mapping file are",
                "final CEDS sectors in the Master_Sector_Level_map.csv..." )

    }

#   B.) Check if all CEDS sectors listed in the MSL are within the RCP sector mapping file
    MSL_CEDS_sectors_not_in_RCP_map <- subset( unique_RCP_map_CEDS_sectors,
                                               !( unique_RCP_map_CEDS_sectors %in% unique_RCP_map_CEDS_sectors ) )

    if( length( MSL_CEDS_sectors_not_in_RCP_map ) != 0 ){

      printLog( MSL_CEDS_sectors_not_in_RCP_map )

      stop( paste0( "The above sectors are in Master_Sector_Level_map.csv but not ",
                    "in the RCP sector mapping file... " ) )

    } else {

      printLog( "All sectors in the in the Master_Sector_Level_map.csv are",
                "in the RCP sector mapping file..." )

    }

# Define regional sectoral plot helper function
  regional_sector_plotting <- function( data_to_graph ){

#   Clean df for plot, and set plot parameters
    plot_df <- data_to_graph %>%
      dplyr::select( Inventory, year, sector, total_emissions ) %>%
      dplyr::mutate( Inventory = as.factor( Inventory ),
                     sector = as.factor( sector ) )

#   Define plot parameters
    max <- 1.2*( max( plot_df$total_emissions ) )

    graph_start <- CEDS_start_year
    graph_end <- CEDS_end_year
    year_breaks <- 25

#   Plot
    plot <- ggplot( plot_df, aes( x = year, y = total_emissions, color = sector,
                                  shape = Inventory, linetype = Inventory ) ) +
      geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
                 size = 1.5 ,aes( x = year,y=total_emissions, color = sector ), alpha = .5 ) +
      geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
                 size = 0.5, aes( x = year, y = total_emissions, color = sector ), alpha = 1 ) +
      scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) ) +
      ggtitle( em ) +
      labs( x = "" , y = 'Emissions [Gg/yr]' )+
      theme( panel.background=element_blank( ),
             panel.grid.minor = element_line( colour = "gray95" ),
             panel.grid.major = element_line( colour = "gray88" ) )+
      scale_y_continuous( limits = c( 0, max ), labels = comma )+
      scale_shape_manual( name = 'Inventory',
                          breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                          values = c( 46, 19 ) )+
      scale_linetype_manual( name= 'Inventory',
                             breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                             values = c( 'solid','solid' ) )+
      guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

      return( plot )

  }

# Define function for subsetting regional by sector data, graphing the data, and
# saving the data and plot to the data and plot lists. Notes:
#   1) region_name: needs to be an RCP region string
#   2) regional_by_sector_full_data: the processed regional by sector data for all RCP regions,
#      from both current and previous versions of CEDS, in long format
#   3) regional_by_sector_full_data_wide: the processed regional by sector data for all RCP regions,
#      from both current and previous versions of CEDS, in wide format
#   4) reg_by_sec_plot_list: the list created in section 2 for the regional by sector plots
#   5) reg_by_sec_plot_data_list: the list created in section 2 for the regional by sector plot data
  graph_and_extract_relevant_regional_by_sec_data <- function( region_name,
                                                               regional_by_sector_full_data = reg_by_sector_long,
                                                               regional_by_sector_full_data_wide = reg_by_sector_wide,
                                                               em_use = em ){

#   Subset specific RCP region data
    region_long_data <- regional_by_sector_full_data %>%
      dplyr::filter( region == region_name )

    region_wide_data <- regional_by_sector_full_data_wide %>%
      dplyr::filter( region == region_name )

#   Graph specific RCP region data
    region_by_sec_plot <- regional_sector_plotting( region_long_data )

#   Add plot and wide df to list
    region_by_sector_plot_and_graph <- list( region_by_sec_plot, region_wide_data )

    return( region_by_sector_plot_and_graph )

  }

# Define legend extraction function from stack exchange
  g_legend<-function( a.gplot ){

    tmp <- ggplot_gtable( ggplot_build( a.gplot ) )
    leg <- which( sapply( tmp$grobs, function( x ) x$name ) == "guide-box" )
    legend <- tmp$grobs[[leg]]
    return( legend )

  }

# ---------------------------------------------------------------------------
# 2. Load CEDS data - previous version and current version

# Print log message about the version of CEDS the user is comparing to
  if( is.null( previous_CEDS_version )  ){

    warning( "previous_CEDS_version was not defined. Comparing current CEDS ",
             "version to the previous CEDS system run..." )

  } else if( !is.null( previous_CEDS_version ) & previous_CEDS_version %!in% available_CEDS_releases ){

    warning( "previous_CEDS_version is defined as a value that is not an available ",
             "CEDS release version (see common_data.R for available versions).",
             "Comparing current CEDS version to the previous CEDS system run..." )
  } else {

    printLog( paste0( "Comparing to CEDS release version ", previous_CEDS_version, "..." ) )

  }

# Start Emissions Loop
#   Create plot and df lists
    global_sector_plot_list <- list( )
    global_sector_plot_list_dfs <- list( )

    top_region_plot_list <- list( )
    top_region_plot_list_dfs <- list( )

    agg_region_plot_list <- list( )
    agg_region_plot_list_dfs <- list( )

    reg1_by_sector_list <- list( )
    reg1_by_sector_df <- list( )

    reg2_by_sector_list <- list( )
    reg2_by_sector_df <- list( )

    africa_by_sector_list <- list( )
    africa_by_sector_df <- list( )

    ROW_by_sector_list <- list( )
    ROW_by_sector_df <- list( )

    global_total_plot_list <- list( )
    global_total_plot_list_dfs <- list( )

    global_fuel_plot_list <- list( )
    global_fuel_plot_list_dfs <- list( )

for( em in seq_along( em_list ) ){

  em <- em_list[ em ]

# for debugging
# em <- "CH4"

# Current CEDS final emissions
  setwd( "../input" )
  current_CEDS_emissions <- readData( 'FIN_OUT', domain_extension = "current-versions/",
                                      paste0( "CEDS_", em, '_emissions_by_country_CEDS_sector_',
                                             current_CEDS_version ) )

  current_CEDS_global_by_fuel <- readData( 'FIN_OUT', domain_extension = "current-versions/",
                                           paste0( "CEDS_", em, '_global_emissions_by_fuel_',
                                                   current_CEDS_version ) )
# Previous CEDS data
#   Load the previous CEDS run if previous_CEDS_version is null or if it is not an available CEDS release version
    if( is.null( previous_CEDS_version ) ) {

      load_previous_run <- TRUE

    } else if( !is.null( previous_CEDS_version ) & previous_CEDS_version %!in% available_CEDS_releases ){

      load_previous_run <- TRUE

    } else {

      load_previous_run <- FALSE

    }

  if( load_previous_run ){

#     Check that previous run exists by country and CEDS sector, and that only one file for a given em exist
      previous_run_fn <- paste0( "CEDS_", em, '_emissions_by_country_CEDS_sector_v_' )
      previous_run_directory <- ( "../final-emissions/previous-versions/" )
      previous_run_fn <- list.files( previous_run_directory, pattern = c( previous_run_fn, "\\dddd" ) )
      previous_run_fn_no_CSV_extension <- gsub( ".csv", "",  previous_run_fn )

      if( length( previous_run_fn ) > 1 ){

        stop( paste0( "There should only be one previous run to compare ", em, " to. Check the final-emissions/previous-versions/ directory..." ) )

      }

      if( length( previous_run_fn ) == 0 ){

       stop( paste0( "There is no previous run to compare to for ", em, ". No futher comparisons will be generated..." ) )

      }

#     Check that previous run exists global by fuel, and that only one file for a given em exist
      previous_run_fn_glb_fuel <- paste0( "CEDS_", em, '_global_emissions_by_fuel_v_' )
      previous_run_fn_glb_fuel <- list.files( previous_run_directory, pattern = c( previous_run_fn_glb_fuel, "\\dddd" ) )
      previous_run_fn_glb_fuel_no_CSV_extension <- gsub( ".csv", "",  previous_run_fn_glb_fuel )

      if( length( previous_run_fn_glb_fuel ) > 1 ){

        stop( paste0( "There should only be one previous run to compare ", em, " to. Check the final-emissions/previous-versions/ directory..." ) )

      }

      if( length( previous_run_fn_glb_fuel ) == 0 ){

        stop( paste0( "There is no previous run to compare to for ", em, ". No futher comparisons will be generated..." ) )

      }

#     Load previous run files
      previous_CEDS_emissions <- readData( 'FIN_OUT', domain_extension = "previous-versions/",
                                           previous_run_fn_no_CSV_extension )

      previous_CEDS_emissions_glb_fuel <- readData( 'FIN_OUT', domain_extension = "previous-versions/",
                                                    previous_run_fn_glb_fuel_no_CSV_extension )

    } else {

#   Load the specified CEDS release
#   TODO: Use CEDS readData instead of read.csv
      setwd( paste0( "../../", CEDS_Data_ROOT, "/emission-archives/", previous_CEDS_version ) )

      if ( previous_CEDS_version == "v2016_07_26" ){

          if( em == "CH4" ){

              previous_CEDS_emissions <- read.csv( paste0( em, "_CEDS_emissions_by_sector_country_v2017_05_18.csv" ) )
              previous_CEDS_emissions_CH4_extension <- read.csv( "CH4_Extension_CEDS_emissions_by_sector_region_v2017_05_18.csv" )

          } else if ( em == "CO2" ) {

              previous_CEDS_emissions <- read.csv( paste0( em, "_CEDS_emissions_by_sector_country_v2017_05_18.csv" ) )

          } else {

            previous_CEDS_emissions <- read.csv( paste0( em, "_CEDS_emissions_by_sector_country_v2016_07_26.csv" ) )

          }

      } else {

        stop( "Options have not yet been set for comparing the current CEDS version to the specified release version (defined as previous_CEDS_version)." )

      }

    }

# ---------------------------------------------------------------------------
# 3. Process current CEDS Emissions Data

# Add RCP regions to current CEDS data
  current_CEDS_region_mapped <- current_CEDS_emissions %>%
    dplyr::filter( ( iso != "global" &
                     sector %!in% c( aviation_sectors, international_shipping_sectors ) ) |
                    ( iso == "global" &
                     sector %in% c( aviation_sectors, international_shipping_sectors ) ) ) %>%   # Remove aviation and int. shipping, unless iso = global
    dplyr::left_join( complete_region_map, by = c( "iso" = "Code" ) ) %>%
    dplyr::rename( RCP_Region = Region ) %>%
    dplyr::select( em, iso, RCP_Region, sector , units, X_all_CEDS_years ) %>%
    dplyr::mutate( RCP_Region = if_else( iso == "global", iso, RCP_Region ) )

# Remove regions not comparing
  if( length( current_CEDS_version_regions_remove ) != 0 ) {

    current_CEDS_region_mapped <- current_CEDS_region_mapped %>%
      dplyr::filter( iso %!in% current_CEDS_version_regions_remove )

  }

# Check that all regions were mapped
  if( any( is.na( current_CEDS_region_mapped$RCP_Region ) ) ){

    stop( "current_CEDS_region_mapped should not have any NAs for RCP_Region after mapping." )

  }

# Add RCP sectors to current CEDS data - remove sectors to remove,
# as well as shipping (and oil tanker loading) and aviation emissions (comparing these for global total only)
  current_CEDS_sectors_mapped_with_ship_and_aviation <- current_CEDS_region_mapped %>%
    dplyr::filter( sector %!in% current_CEDS_version_sectors_to_remove ) %>%
    dplyr::left_join( sector_map, by = "sector" ) %>%
    dplyr::rename( RCP_Sector = RCP ) %>%
    dplyr::select( em, iso, RCP_Region, sector, RCP_Sector , units, X_all_CEDS_years )

  if( any( is.na( current_CEDS_sectors_mapped_with_ship_and_aviation$RCP_Sector ) ) ){

        stop( "current_CEDS_sectors_mapped_with_ship_and_aviation should not have any NAs for RCP_sector after mapping." )

  }

# Make a version without aviation and international shipping (as well as oil tanker loading)
  current_CEDS_sectors_mapped <- current_CEDS_sectors_mapped_with_ship_and_aviation %>%
    dplyr::filter( sector %!in% c( aviation_sectors, international_shipping_sectors ) )

# ---------------------------------------------------------------------------
# 4. Process previous CEDS Emissions Data

# Initial Cleaning for CEDS version v2016_07_26 --- change variable names, add units column, change variable types, fix sector names
  if( load_previous_run ){

      previous_CEDS_emissions_clean <- previous_CEDS_emissions

  } else if( previous_CEDS_version == "v2016_07_26" ){

      previous_CEDS_emissions_clean <- previous_CEDS_emissions %>%
        dplyr::rename( iso = country ) %>%
        dplyr::mutate( units = "kt" ,
                       sector = as.character( sector ),
                       iso = as.character( iso ) ) %>%
        dplyr::mutate( sector = if_else( sector == "2Ax_Other-minerals", "2A6_Other-minerals",
                                if_else( sector == "2D_Chemical-products-manufacture-processing",
                                                   "2D3_Chemical-products-manufacture-processing",
                                if_else( sector == "2D_Other-product-use", "2D3_Other-product-use",
                                if_else( sector == "5C_Waste-combustion", "5C_Waste-incineration", sector ) ) ) ) )
  } else {

    previous_CEDS_emissions_clean <- previous_CEDS_emissions

  }

# Make an object with all previous years that are within current CEDS years
# (assumes current emissions can go out futher in time than previous emissions)
  previous_CEDS_years <- subset( colnames( previous_CEDS_emissions_clean ),
                                 isXYear( colnames( previous_CEDS_emissions_clean ) ) )

  previous_CEDS_years_use <- subset( previous_CEDS_years, previous_CEDS_years %in% X_all_CEDS_years )

# Add RCP regions to previous CEDS data
  previous_CEDS_region_mapped <- previous_CEDS_emissions_clean %>%
    dplyr::filter( ( iso != "global" &
                     sector %!in% c( aviation_sectors, international_shipping_sectors ) ) |
                   ( iso == "global" &
                     sector %in% c( aviation_sectors, international_shipping_sectors ) ) ) %>%   # Remove aviation and int. shipping, unless iso = global
    dplyr::left_join( complete_region_map, by = c( "iso" = "Code" ) ) %>%
    dplyr::rename( RCP_Region = Region ) %>%
    dplyr::select( em, iso, RCP_Region, sector , units, previous_CEDS_years_use ) %>%
    dplyr::mutate( RCP_Region = if_else( iso == "global", iso, RCP_Region ) )

# Remove regions not comparing
  if( length( previous_CEDS_version_regions_remove ) != 0 ) {

    previous_CEDS_region_mapped <- previous_CEDS_region_mapped %>%
      dplyr::filter( iso %!in% previous_CEDS_version_regions_remove )

  }

# Check that all regions were mapped
  if( any( is.na( previous_CEDS_region_mapped$RCP_Region ) ) ){

    stop( "previous_CEDS_sectors_mapped should not have any NAs for RCP_Region after mapping." )

  }

# Add RCP sectors to previous CEDS data  - remove sectors to remove,
# as well as shipping (and oil tanker loading) and aviation emissions (comparing these for global total only)
  previous_CEDS_sectors_mapped_with_ship_and_aviation <- previous_CEDS_region_mapped %>%
    dplyr::filter( sector %!in% previous_CEDS_version_sectors_to_remove ) %>%
    dplyr::left_join( sector_map, by = "sector" ) %>%
    dplyr::rename( RCP_Sector = RCP ) %>%
    dplyr::select( em, iso, RCP_Region, sector, RCP_Sector , units, previous_CEDS_years_use )

  if( any( is.na( previous_CEDS_sectors_mapped_with_ship_and_aviation$RCP_Sector ) ) ){

    stop( "previous_CEDS_sectors_mapped_with_ship_and_aviation should not have any NAs for RCP_sector after mapping." )

  }

# Make a version without aviation and international shipping (as well as oil tanker loading)
  previous_CEDS_sectors_mapped <- previous_CEDS_sectors_mapped_with_ship_and_aviation %>%
    dplyr::filter( sector %!in% c( aviation_sectors, international_shipping_sectors ) ) %>%
    dplyr::select( em, iso, RCP_Region, sector, RCP_Sector , units, previous_CEDS_years_use )

# ---------------------------------------------------------------------------
# 5.  Region Comparisons

# Check that all desired regions to graph by sector are RCP regions
  if( any( regions_to_compare %!in% complete_region_map$Region ) ){

    print( sort( unique( regions_to_compare$Region ) ) )

    stop( "The user has defined a region to graph by sector which is not an RCP region. ",
          "Please select from the above RCP regions..." )

  }

# Prepare current CEDS Data for regional comparison
  region_current_ceds <- current_CEDS_sectors_mapped %>%
    dplyr::select( RCP_Region, X_all_CEDS_years ) %>%
    dplyr::group_by( RCP_Region  ) %>%
    dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
    dplyr::rename( region = RCP_Region ) %>%
    dplyr::mutate( Inventory = paste0( "CEDS_", current_CEDS_version ) ) %>%
    dplyr::ungroup( ) %>%
    dplyr::select( region, Inventory, X_all_CEDS_years )

  region_current_ceds_long <- region_current_ceds %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years )

# Prepare previous CEDS Data for regional comparison
  if( is.null( previous_CEDS_version ) ){

    previous_CEDS_version <- "vPrevious_system_run"

  }

  region_previous_ceds <- previous_CEDS_sectors_mapped %>%
    dplyr::select( RCP_Region, previous_CEDS_years_use ) %>%
    dplyr::group_by( RCP_Region  ) %>%
    dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
    dplyr::rename( region = RCP_Region ) %>%
    dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) ) %>%
    dplyr::ungroup( )

  X_all_CEDS_years_previous_version <- previous_CEDS_years_use

# If em is CH4 and comparing to release v2016_07_26, then process and add extended emissions
  if( em == "CH4" & previous_CEDS_version == "v2016_07_26" ){

    previous_CEDS_emissions_CH4_extension_no_bunkers <- previous_CEDS_emissions_CH4_extension %>%
      dplyr::mutate( RCP_Sector = as.character( RCP_Sector ),
                     RCP_Region = as.character( RCP_Region ) ) %>%
      dplyr::filter( RCP_Sector %!in% c( "International-shipping", "Aviation" ) ) %>%
      dplyr::mutate( RCP_Sector = if_else( RCP_Sector == "Fossil-fuel-fires", "ENE", RCP_Sector ) ) %>% # Mapping here as RCP map won't be changed
                                                                                                        # given that the RCP map is used for other comparisons
                                                                                                        # which don't use fossil fuel fires
      dplyr::rename( region = RCP_Region ) %>%
      dplyr::select( -RCP_Sector, -X1970 ) %>%
      dplyr::group_by( region ) %>%
      dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
      dplyr::ungroup( ) %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) )

    X_all_CEDS_years_previous_version_temp <- unique( c( paste0( "X", seq( from = 1850, to = 1970, by = 10 ) ), previous_CEDS_years_use ) ) # Unique call to remove duplicate 1970

    X_all_CEDS_years_previous_version <- subset( X_all_CEDS_years_previous_version_temp,
                                                 X_all_CEDS_years_previous_version_temp %in% X_all_CEDS_years )

    region_previous_ceds <- region_previous_ceds %>%
      dplyr::left_join( previous_CEDS_emissions_CH4_extension_no_bunkers, by = c( "region", "Inventory" ) ) %>%
      dplyr::select( region, Inventory, X_all_CEDS_years_previous_version )

  }

  region_previous_ceds_long <- region_previous_ceds %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years_previous_version )

# Combine current and previous CEDS Data into long form, and perform final data cleaning for graph (filter for years of interest)
  region_long <- dplyr::bind_rows( region_current_ceds_long, region_previous_ceds_long ) %>%
    dplyr::filter( year %in% X_all_CEDS_years ) %>%
    dplyr::mutate( year = gsub( "X", "", year ) ) %>%
    dplyr::mutate( year = as.numeric( year ) )

# If CH4 start year is not the same as the start year for other ems, then filter out those years
if( em == "CH4" & !is.invalid( CH4_start_year ) ){

  if( CEDS_start_year != CH4_start_year ){

    region_long <- region_long %>%
      dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

  }

}

# Combine current and previous CEDS Data into wide form, and perform final data cleaning for graph
  region <- dplyr::bind_rows( region_current_ceds, region_previous_ceds ) %>%
    dplyr::select( region, Inventory,  X_all_CEDS_years ) %>%
    dplyr::arrange( region, Inventory )

# The following chunk could be used in the future alternatively if one wanted to plot the top 5 regions
# Create order of plots
#   regions_list <- region_long[ ,c( 'region', 'total_emissions' ) ]
#   regions_list <- regions_list[ order( -regions_list$total_emissions ),]
#   regions_list_order <- unique( regions_list$region )
#   regions_df_order <- data.frame( region = regions_list_order,
#                                   group = unlist( lapply( X = 1 : 6, FUN = rep, times = 7 ) )[ 1 : 39 ] )
#
# # Plot only the select 5 regions
#   plot_regions <- dplyr::slice( regions_df_order, 1:5 ) %>%
#       dplyr::mutate( region = as.character( region ) )

  # plot_regions <- c( plot_regions$region )

# Clean df for plot, and set plot parameters
  plot_df <- region_long %>%
    dplyr::filter( region %in% regions_to_compare ) %>%
    dplyr::select( Inventory, year, region, total_emissions ) %>%
    dplyr::mutate( Inventory = as.factor( Inventory ),
                   region = as.factor( region ) )

  max <- 1.2*( max( plot_df$total_emissions ) )

  graph_start <- CEDS_start_year
  graph_end <- CEDS_end_year
  year_breaks <- 25

# Plot
  plot <- ggplot( plot_df, aes( x = year, y = total_emissions, color = region,
                                shape = Inventory, linetype = Inventory ) ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
               size = 1.5, aes( x = year,y = total_emissions, color = region ), alpha = .5 ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
               size = 0.5, aes( x = year, y = total_emissions, color = region ), alpha = 1 ) +
    scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) ) +
    ggtitle( em )+
    labs( x= "" , y= 'Emissions [Gg/yr]' )+
    theme( panel.background=element_blank(),
           panel.grid.minor = element_line( colour="gray95" ),
           panel.grid.major = element_line( colour="gray88" ) )+
    scale_y_continuous( limits = c( 0, max ), labels = comma )+
    scale_color_discrete( name = 'Region')+
    scale_shape_manual( name= 'Inventory',
                        breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                        values = c( 46, 19 ) ) +
    scale_linetype_manual( name= 'Inventory',
                           breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                           values = c( 'solid','solid' ) ) +
    guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

# Add plot and wide df to list
  top_region_plot_list[[ em ]] <- plot
  top_region_plot_list_dfs[[ em ]] <- region

# ---------------------------------------------------------------------------
# 6.  Aggregate regions comparison

# Create column with aggregate regions and check that all regions are mapped to these aggregate regions
  north_america <- c( "Canada", "Mexico", "USA" )
  europe <- c( "Baltic States", "Central Europe", "France", "Germany", "Greenland", "Italy", "Turkey",
               "Ukraine+", "United Kingdom", "Western Europe" )
  africa_ME_Samerica <- c( "Argentina", "Brazil", "Central America", "Eastern Africa", "Middle East",
                           "Northern Africa",  "South Africa", "South America", "Southern Africa",
                           "Venezuela", "Western Africa" )
  russia <- c( "Russia+" )
  china <- c( "China+" )
  india <- c( "India" )
  aus_japan_NZ <- c( "Australia", "Japan", "New Zealand" )
  rest_of_asia_pac_isl <- c( "Asia-Stan", "Indonesia+", "North Korea",  "Oceania",  "South Asia",
                             "South Korea", "Southeastern Asia", "Taiwan",  "Thailand" )

  agg_region_mapped <- region %>%
    dplyr::mutate( agg_region = if_else( region %in% north_america, "North America", region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% europe, "Europe", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% africa_ME_Samerica, "Africa, Cen. and S. America, and Middle East", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% russia, "Russia+", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% china, "China+", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% india, "India", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% aus_japan_NZ, "Australia, Japan, and New Zealand", agg_region ) ) %>%
    dplyr::mutate( agg_region = if_else( region %in% rest_of_asia_pac_isl, "Rest of Asia and Pacific Islands", agg_region ) )

  if( any( is.na( agg_region_mapped$agg_region ) ) ){

    stop( "All RCP regions should be mapped to an aggregate region. Please check the data and version comparison script..." )

  }

# Aggregate by Inventory and agg_region
  agg_region <- agg_region_mapped %>%
    dplyr::select( agg_region, Inventory, X_all_CEDS_years ) %>%
    dplyr::group_by( agg_region, Inventory ) %>%
    dplyr::summarize_all( sum, na.rm = TRUE ) %>%
    dplyr::ungroup( )

# Reset values to NA from 0 for years which don't exist in previous CEDS data
# Assumes that current data can go out futher in time than previous data,
# but not the opposite
  if( last( X_all_CEDS_years ) != last( X_all_CEDS_years_previous_version ) ){

    last_previous_year <- gsub( "X", "", last( X_all_CEDS_years_previous_version ) )
    last_current_year <- gsub( "X", "", last( X_all_CEDS_years ) )
    missing_recent_years <- paste0( "X", last_previous_year : last_current_year )

    agg_region <- agg_region %>%
      dplyr::mutate_at( .vars = missing_recent_years, .funs = funs( if_else(
                        Inventory ==  paste0( "CEDS_", previous_CEDS_version ) & . == 0,
                                                                             NA_real_, . ) ) )

  }

# Need to reset all NA years to NA for the CMIP CEDS release, if being used
  if( previous_CEDS_version == "v2016_07_26" ){

    CMIP_release_NA_years <- agg_region_mapped %>%
      dplyr::filter( Inventory == "CEDS_v2016_07_26" ) %>%
      dplyr::select_if( all.na )

    CMIP_release_NA_year_cols <- colnames( CMIP_release_NA_years )

      if( length( CMIP_release_NA_year_cols ) != 0 ){

        agg_region_fixed <- agg_region %>%
          dplyr::mutate_at( CMIP_release_NA_year_cols, funs( if_else( Inventory == "CEDS_v2016_07_26", NA_real_, . ) ) )

      } else {

        agg_region_fixed <- agg_region

      }

  } else {

    agg_region_fixed <- agg_region

  }

# Make long for graph, remove X in years and make them numeric, filter for years of interest and
# years which are not NA (CMIP CEDs release would have NA values in certain years)
  agg_region_long <- agg_region_fixed %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years ) %>%
    dplyr::filter( year %in% X_all_CEDS_years,
                   !is.na( total_emissions ) ) %>%
    dplyr::mutate( year = gsub( "X", "", year ) ) %>%
    dplyr::mutate( year = as.numeric( year ) )

# If CH4 start year is not the same as the start year for other ems, then filter out those years
  if( em == "CH4" & !is.invalid( CH4_start_year ) ){

    if( CEDS_start_year != CH4_start_year ){

      agg_region_long <- agg_region_long %>%
        dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

    }

  }

# Clean df for plot, and set plot parameters
  plot_df <- agg_region_long %>%
    dplyr::select( Inventory, year, agg_region, total_emissions ) %>%
    dplyr::mutate( Inventory = as.factor( Inventory ),
                   agg_region = as.factor( agg_region ) )

  max <- 1.2*( max( plot_df$total_emissions ) )

  graph_start <- CEDS_start_year
  graph_end <- CEDS_end_year
  year_breaks <- 25

# Plot
  plot <- ggplot( plot_df, aes( x = year, y = total_emissions, color = agg_region,
                                shape = Inventory, linetype = Inventory ) ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
               size = 1.5, aes( x = year,y = total_emissions, color = agg_region ), alpha = .5 ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
               size = 0.5, aes( x = year, y = total_emissions, color = agg_region ), alpha = 1 ) +
    scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) ) +
    ggtitle( em )+
    labs( x= "" , y= 'Emissions [Gg/yr]' )+
    theme( panel.background=element_blank(),
           panel.grid.minor = element_line( colour="gray95" ),
           panel.grid.major = element_line( colour="gray88" ) )+
    scale_y_continuous( limits = c( 0, max ),labels = comma )+
    scale_color_discrete( name = 'Region')+
    scale_shape_manual( name= 'Inventory',
                        breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                        values = c( 46, 19 ) ) +
    scale_linetype_manual( name= 'Inventory',
                           breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                           values = c( 'solid','solid' ) ) +
    guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

# Add plot and wide df to list
  agg_region_plot_list[[ em ]] <- plot
  agg_region_plot_list_dfs[[ em ]] <- agg_region_fixed

# ---------------------------------------------------------------------------
# 7.  Process and graph data for regional by sector comparisons

if( length( RCP_regions_for_reg_by_sec_comparison ) > 0 ){ # If user defined RCP regions to graph by sector

#   Stop if the user defined more than 2 RCP regions to graph by sector, as the
#   script is currently configured to only allow for 2 user selections.
    if( length( RCP_regions_for_reg_by_sec_comparison ) > 2 ){

      stop( "The user has selected more than 2 regions to graph by sector, but ",
            script_name, " is only configured for a maximum of 2 user selected regions. ",
            "Please redefine RCP_regions_for_reg_by_sec_comparison in Section 0.5 with ",
            "at most 2 regions..." )

    }

#   Check that all desired regions to graph by sector are RCP regions
    if( any( RCP_regions_for_reg_by_sec_comparison %!in% complete_region_map$Region ) ){

      print( sort( unique( complete_region_map$Region ) ) )

      stop( "The user has defined a region to graph by sector which is not an RCP region. ",
            "Please select from the above RCP regions..." )

    }

# Prepare data - User select RCP regions, Africa (all African RCP regions as once region)
# and ROW region

#   Define mapping for regions that are not RCP regions that may want to be graphed
    african_RCP_regions <- c(  "Eastern Africa", "Northern Africa", "South Africa",
                               "Southern Africa", "Western Africa" )

#   Prepare current CEDS Data for sectoral comparison
    reg_sec_current_ceds <- current_CEDS_sectors_mapped_with_ship_and_aviation %>%
      dplyr::mutate( RCP_Region = if_else( RCP_Region %in% RCP_regions_for_reg_by_sec_comparison,
                                           RCP_Region,
                                           if_else( RCP_Region %in% african_RCP_regions,
                                                    "Africa", "Rest of World" ) ) ) %>%
      dplyr::select( RCP_Region, RCP_Sector, X_all_CEDS_years ) %>%
      dplyr::group_by( RCP_Region, RCP_Sector  ) %>%
      dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
      dplyr::rename( sector = RCP_Sector,
                     region = RCP_Region ) %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", current_CEDS_version ) ) %>%
      dplyr::ungroup( ) %>%
      dplyr::select( region, sector, Inventory, X_all_CEDS_years )

#   Prepare previous CEDS Data for sectoral comparison
    reg_sec_previous_ceds <- previous_CEDS_sectors_mapped_with_ship_and_aviation %>%
      dplyr::mutate( RCP_Region = if_else( RCP_Region %in% RCP_regions_for_reg_by_sec_comparison,
                                           RCP_Region,
                                           if_else( RCP_Region %in% african_RCP_regions,
                                                    "Africa", "Rest of World" ) ) ) %>%
      dplyr::select( RCP_Region, RCP_Sector, previous_CEDS_years_use ) %>%
      dplyr::group_by( RCP_Region, RCP_Sector  ) %>%
      dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
      dplyr::rename( sector = RCP_Sector,
                     region = RCP_Region ) %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) ) %>%
      dplyr::ungroup( ) %>%
      dplyr::select( region, sector, Inventory, previous_CEDS_years_use )

#   If em is CH4 and comparing to release v2016_07_26, then process and add extended emissions
    if( em == "CH4" & previous_CEDS_version == "v2016_07_26" ){

      reg_sec_previous_ceds_CH4_extension <- previous_CEDS_emissions_CH4_extension %>%
        dplyr::mutate( RCP_Sector = as.character( RCP_Sector ),
                       RCP_Region = as.character( RCP_Region ) ) %>%
        dplyr::mutate( RCP_Sector = if_else( RCP_Sector == "International-shipping", "INT. SHIPPING",
                                             if_else( RCP_Sector == "Aviation", "AVIATION", RCP_Sector ) ) )  %>%
        dplyr::mutate( RCP_Sector = if_else( RCP_Sector == "Fossil-fuel-fires", "ENE", RCP_Sector ) ) %>%
        dplyr::mutate( RCP_Region = if_else( RCP_Region %in% RCP_regions_for_reg_by_sec_comparison,
                                             RCP_Region,
                                             if_else( RCP_Region %in% african_RCP_regions,
                                                      "Africa", "Rest of World" ) ) ) %>%
        dplyr::select( -X1970 ) %>%
        dplyr::group_by( RCP_Region, RCP_Sector  ) %>%
        dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
        dplyr::rename( sector = RCP_Sector,
                       region = RCP_Region ) %>%
        dplyr::ungroup( ) %>%
        dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) )

      reg_sec_previous_ceds <- reg_sec_previous_ceds %>%
        dplyr::left_join( reg_sec_previous_ceds_CH4_extension, by = c( "region", "sector", "Inventory" ) ) %>%
        dplyr::select( region, sector, Inventory, X_all_CEDS_years_previous_version )

    }

# Combine data

#   Combine in wide format
    reg_by_sector_wide <- dplyr::bind_rows( reg_sec_current_ceds, reg_sec_previous_ceds ) %>%
      dplyr::select( region, sector, Inventory,  X_all_CEDS_years ) %>%
      dplyr::arrange( region, sector, Inventory )

#   Create long format data frame
    reg_by_sector_long <- reg_by_sector_wide %>%
      tidyr::gather( year, total_emissions, X_all_CEDS_years ) %>%
      dplyr::filter( year %in% X_all_CEDS_years ) %>%
      dplyr::mutate( year = gsub( "X", "", year ) ) %>%
      dplyr::mutate( year = as.numeric( year ) )

#   If CH4 start year is not the same as the start year for other ems, then filter out those years
    if( em == "CH4" & !is.invalid( CH4_start_year ) ){

      if( CEDS_start_year != CH4_start_year ){

        reg_by_sector_long <- reg_by_sector_long %>%
          dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

      }

    }

#   Graph data for Africa
    africa_data_and_plot <- graph_and_extract_relevant_regional_by_sec_data( region_name =  "Africa" )
    africa_by_sector_list[[em]] <- africa_data_and_plot[[1]]
    africa_by_sector_df[[em]] <- africa_data_and_plot[[2]]

#   Graph emissions by sector for the first RCP region
    RCP_reg1_reg_by_sec <- RCP_regions_for_reg_by_sec_comparison[[1]]
    reg1_data_and_plot <- graph_and_extract_relevant_regional_by_sec_data( region_name =  RCP_reg1_reg_by_sec )
    reg1_by_sector_list[[em]] <- reg1_data_and_plot[[1]]
    reg1_by_sector_df[[em]] <- reg1_data_and_plot[[2]]

#   Graph emissions by sector for the second RCP region, if 2 regions were provided by the user
    if( length( RCP_regions_for_reg_by_sec_comparison ) == 2 ){

      RCP_reg2_reg_by_sec <- RCP_regions_for_reg_by_sec_comparison[[2]]
      reg2_data_and_plot <- graph_and_extract_relevant_regional_by_sec_data( region_name = RCP_reg2_reg_by_sec )
      reg2_by_sector_list[[em]] <- reg2_data_and_plot[[1]]
      reg2_by_sector_df[[em]] <- reg2_data_and_plot[[2]]

    }

#   Graph data for Rest of the World
    ROW_data_and_plot <- graph_and_extract_relevant_regional_by_sec_data( region_name = "Rest of World" )
    ROW_by_sector_list[[em]] <- ROW_data_and_plot[[1]]
    ROW_by_sector_df[[em]] <- ROW_data_and_plot[[2]]

  }

# ---------------------------------------------------------------------------
# 8.  Sector Comparison

# Prepare current CEDS Data for sectoral comparison
  sector_current_ceds <- current_CEDS_sectors_mapped_with_ship_and_aviation %>%
    dplyr::select( RCP_Sector, X_all_CEDS_years ) %>%
    dplyr::group_by( RCP_Sector  ) %>%
    dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
    dplyr::rename( sector = RCP_Sector ) %>%
    dplyr::mutate( Inventory = paste0( "CEDS_", current_CEDS_version ) ) %>%
    dplyr::ungroup( ) %>%
    dplyr::select( sector, Inventory, X_all_CEDS_years )

  sector_current_ceds_long <- sector_current_ceds %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years )

# Prepare previous CEDS Data for sectoral comparison
  sector_previous_ceds <- previous_CEDS_sectors_mapped_with_ship_and_aviation %>%
    dplyr::select( RCP_Sector, previous_CEDS_years_use ) %>%
    dplyr::group_by( RCP_Sector  ) %>%
    dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
    dplyr::rename( sector = RCP_Sector ) %>%
    dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) ) %>%
    dplyr::ungroup( )

# If em is CH4 and comparing to release v2016_07_26, then process and add extended emissions
  if( em == "CH4" & previous_CEDS_version == "v2016_07_26" ){

    previous_CEDS_emissions_CH4_extension_no_bunkers_global <- previous_CEDS_emissions_CH4_extension %>%
      dplyr::mutate( RCP_Sector = as.character( RCP_Sector ),
                     RCP_Region = as.character( RCP_Region ) ) %>%
      dplyr::mutate( RCP_Sector = if_else( RCP_Sector == "International-shipping", "INT. SHIPPING",
                                  if_else( RCP_Sector == "Aviation", "AVIATION", RCP_Sector ) ) )  %>%
      dplyr::mutate( RCP_Sector = if_else( RCP_Sector == "Fossil-fuel-fires", "ENE", RCP_Sector ) ) %>%
      dplyr::rename( sector = RCP_Sector ) %>%
      dplyr::select( -RCP_Region, -X1970 ) %>%
      dplyr::group_by( sector ) %>%
      dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) ) %>%
      dplyr::ungroup( ) %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) )

    sector_previous_ceds <- sector_previous_ceds %>%
      dplyr::left_join( previous_CEDS_emissions_CH4_extension_no_bunkers_global, by = c( "sector", "Inventory" ) ) %>%
      dplyr::select( sector, Inventory, X_all_CEDS_years_previous_version )

  }

  sector_previous_ceds_long <- sector_previous_ceds %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years_previous_version )

# Combine current and previous CEDS Data into long form, and perform final data cleaning for graph
  sector_long <- dplyr::bind_rows( sector_current_ceds_long, sector_previous_ceds_long ) %>%
    dplyr::filter( year %in% X_all_CEDS_years ) %>%
    dplyr::mutate( year = gsub( "X", "", year ) ) %>%
    dplyr::mutate( year = as.numeric( year ) )

# If CH4 start year is not the same as the start year for other ems, then filter out those years
  if( em == "CH4" & !is.invalid( CH4_start_year ) ){

    if( CEDS_start_year != CH4_start_year ){

      sector_long <- sector_long %>%
        dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

    }

  }

# Combine current and previous CEDS Data into wide form, and perform final data cleaning for graph
  sector <- dplyr::bind_rows( sector_current_ceds, sector_previous_ceds ) %>%
    dplyr::select( sector, Inventory,  X_all_CEDS_years ) %>%
    dplyr::arrange( sector, Inventory )

# Clean df for plot, and set plot parameters
  plot_df <- sector_long %>%
    dplyr::select( Inventory, year, sector, total_emissions ) %>%
    dplyr::mutate( Inventory = as.factor( Inventory ),
                   sector = as.factor( sector ) )

  max <- 1.2*( max( plot_df$total_emissions ) )

  graph_start <- CEDS_start_year
  graph_end <- CEDS_end_year
  year_breaks <- 25

# Plot
  plot <- ggplot( plot_df, aes( x = year,y = total_emissions, color = sector,
                              shape = Inventory, linetype = Inventory ) ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
               size = 1.5 ,aes( x = year,y=total_emissions, color = sector ), alpha = .5 ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
               size = 0.5, aes( x = year, y = total_emissions, color = sector ), alpha = 1 ) +
    scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) )+
    ggtitle( em )+
    labs( x = "" , y = 'Emissions [Gg/yr]' )+
    theme( panel.background=element_blank( ),
           panel.grid.minor = element_line( colour = "gray95" ),
           panel.grid.major = element_line( colour = "gray88" ) )+
    scale_y_continuous( limits = c( 0, max ), labels = comma )+
    scale_shape_manual( name = 'Inventory',
                        breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                        values = c( 46, 19 ) )+
    scale_linetype_manual( name= 'Inventory',
                           breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                           values = c( 'solid','solid' ) )+
    guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

# Add plot and wide df to list
  global_sector_plot_list[[ em ]] <- plot
  global_sector_plot_list_dfs[[ em ]] <- sector

# ---------------------------------------------------------------------------
# 9.  Global total comparison

# Create global total df
  global_current_ceds <- sector_current_ceds %>%
     dplyr::select( -sector ) %>%
     dplyr::group_by( Inventory ) %>%
     dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) )

  global_previous_ceds <- sector_previous_ceds %>%
     dplyr::select( -sector ) %>%
     dplyr::group_by( Inventory ) %>%
     dplyr::summarize_all( funs( sum( ., na.rm = TRUE ) ) )

  global_total_wide <- dplyr::bind_rows( global_current_ceds, global_previous_ceds ) %>%
    dplyr::select( Inventory,  X_all_CEDS_years ) %>%
    dplyr::arrange( Inventory )

  global_total_long <- global_total_wide %>%
    tidyr::gather( year, total_emissions, X_all_CEDS_years ) %>%
    dplyr::filter( year %in% X_all_CEDS_years ) %>%
    dplyr::mutate( year = gsub( "X", "", year ) ) %>%
    dplyr::mutate( year = as.numeric( year ) ) %>%
    dplyr::filter( !is.na( total_emissions ) )

# If CH4 start year is not the same as the start year for other ems, then filter out those years
  if( em == "CH4" & !is.invalid( CH4_start_year ) ){

    if( CEDS_start_year != CH4_start_year ){

      global_total_long <- global_total_long %>%
        dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

    }

  }

# Clean df for plot, and set plot parameters
  plot_df <- global_total_long %>%
    dplyr::mutate( Inventory = as.factor( Inventory ) )

  max <- 1.2*( max( plot_df$total_emissions ) )

  graph_start <- CEDS_start_year
  graph_end <- CEDS_end_year
  year_breaks <- 25

# Plot
  plot <- ggplot( plot_df, aes( x = year, y = total_emissions, color = Inventory,
                                shape = Inventory, linetype = Inventory ) ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
               size = 1.5 ,aes( x = year,y = total_emissions, color = Inventory ), alpha = .5 ) +
    geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
               size = 0.5, aes( x = year, y = total_emissions, color = Inventory ), alpha = 1 ) +
    scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) )+
    ggtitle( em )+
    labs( x = "" , y = 'Emissions [Gg/yr]' )+
    theme( panel.background=element_blank( ),
           panel.grid.minor = element_line( colour = "gray95" ),
           panel.grid.major = element_line( colour = "gray88" ) )+
    scale_y_continuous( limits = c( 0, max ), labels = comma )+
    scale_shape_manual( name = 'Inventory',
                        breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                        values = c( 46, 19 ) )+
    scale_linetype_manual( name= 'Inventory',
                           breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                           values = c( 'solid','solid' ) )+
    guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

# Add plot and wide df to list
  global_total_plot_list[[ em ]] <- plot
  global_total_plot_list_dfs[[ em ]] <- global_total_wide

# ---------------------------------------------------------------------------
# 10.  Global total by fuel comparison

  if( load_previous_run |  previous_CEDS_version != "v2016_07_26" ){

#   Combine previous and current CEDS runs - wide
    current_CEDS_global_by_fuel_clean <- current_CEDS_global_by_fuel %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", current_CEDS_version ) ) %>%
      dplyr::select( Inventory, em, fuel, units, X_all_CEDS_years )

    previous_CEDS_emissions_glb_fuel_clean <- previous_CEDS_emissions_glb_fuel %>%
      dplyr::mutate( Inventory = paste0( "CEDS_", previous_CEDS_version ) ) %>%
      dplyr::select( Inventory, em, fuel, units, X_all_CEDS_years_previous_version )

    global_by_fuel <- dplyr::bind_rows( current_CEDS_global_by_fuel_clean,  previous_CEDS_emissions_glb_fuel_clean)

#   Combine previous and current CEDS runs - long
    current_CEDS_global_by_fuel_long <- current_CEDS_global_by_fuel_clean %>%
      tidyr::gather( year, total_emissions, X_all_CEDS_years ) %>%
      dplyr::select( Inventory, em, fuel, units, year, total_emissions )

    previous_CEDS_emissions_glb_fuel_long <- previous_CEDS_emissions_glb_fuel_clean %>%
      tidyr::gather( year, total_emissions, X_all_CEDS_years_previous_version ) %>%
      dplyr::select( Inventory, em, fuel, units, year, total_emissions )

    global_by_fuel_long <- dplyr::bind_rows( current_CEDS_global_by_fuel_long, previous_CEDS_emissions_glb_fuel_long ) %>%
      dplyr::mutate( year = gsub( "X", "", year ) ) %>%
      dplyr::mutate( year = as.numeric( year ) ) %>%
      dplyr::filter( !is.na( total_emissions ) )

# If CH4 start year is not the same as the start year for other ems, then filter out those years
  if( em == "CH4" & !is.invalid( CH4_start_year ) ){

    if( CEDS_start_year != CH4_start_year ){

      global_by_fuel_long <- global_by_fuel_long %>%
          dplyr::mutate( total_emissions = if_else( year < CH4_start_year, NA_real_, total_emissions ) )

    }

  }

#   Clean df for plot, and set plot parameters
    plot_df <- global_by_fuel_long %>%
      dplyr::mutate( Inventory = as.factor( Inventory ) )

    max <- 1.2*( max( plot_df$total_emissions ) )

    graph_start <- CEDS_start_year
    graph_end <- CEDS_end_year
    year_breaks <- 25

#   Plot
    plot <- ggplot( plot_df, aes( x = year, y = total_emissions, color = fuel,
                                  shape = Inventory, linetype = Inventory ) ) +
      geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", current_CEDS_version ) ),
                 size = 1.5 ,aes( x = year,y = total_emissions, color = fuel ), alpha = .5 ) +
      geom_line( data = dplyr::filter( plot_df, Inventory == paste0( "CEDS_", previous_CEDS_version ) ),
                 size = 0.5, aes( x = year, y = total_emissions, color = fuel ), alpha = 1 ) +
      scale_x_continuous( breaks = seq( from = graph_start, to = graph_end, by = year_breaks ) )+
      ggtitle( em )+
      labs( x = "" , y = 'Emissions [Gg/yr]' )+
      theme( panel.background=element_blank( ),
             panel.grid.minor = element_line( colour = "gray95" ),
             panel.grid.major = element_line( colour = "gray88" ) )+
      scale_y_continuous( limits = c( 0, max ), labels = comma )+
      scale_shape_manual( name = 'Inventory',
                          breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                          values = c( 46, 19 ) )+
      scale_linetype_manual( name= 'Inventory',
                             breaks = c( paste0( "CEDS_", current_CEDS_version ), paste0( "CEDS_", previous_CEDS_version ) ),
                             values = c( 'solid','solid' ) )+
      guides( linetype = guide_legend( override.aes = list( size = c( 1.5, 0.5 ) ) ) )

  # Add plot and wide df to list
    global_fuel_plot_list[[ em ]] <- plot
    global_fuel_plot_list_dfs[[ em ]] <- global_by_fuel

  }

# End emissions loop - reset wd if comparing to CEDS release 1 (CMIP release)
  if( previous_CEDS_version == "v2016_07_26" ){

    setwd( paste0("../../../", CEDS_ROOT, "/input" ) )

  }

}

# ---------------------------------------------------------------------------
# 11. Save Data and Graph
# Note: The graph PDFs are by default configured to include all CEDS emission
#       species (9 ems). If less are used, then delete the extra assignments
#       within the grid.arrange() calls below. For instance, if you did not
#       include CO2 and CH4 in your emission species within section 0.5,
#       then you would need to delete top_region_plot_list[[8]] and top_region_plot_list[[9]].
#       This manual deletion would then need to be repeated for all other grid.arrange()
#       calls below. Additionally, you may want to remove any "blank" objects within
#       the grid.arrange() call, as well as modify the ncols parameter.
# TODO: Automate the ability to save plot lists of varying lengths (if not all CEDS
#       emission species are utilized). Using grobs = <list_of_plots> within grid.arrange()
#       works, but then does not allow for the legend placement (even if the object legend
#       is added to the list of plots being arranged)
# TODO: Use CEDS writeData instead of write.xlsx
setwd( "../final-emissions/diagnostics/version-comparisons" )

# 5 regions
  legend <- g_legend( top_region_plot_list[[1]] )
  top_region_plot_list <- lapply( top_region_plot_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Select_CMIP_regions-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper='special' )

  if( include_titles_on_graphs ){
    grid.arrange( top_region_plot_list[[1]], top_region_plot_list[[2]], top_region_plot_list[[3]],
                  top_region_plot_list[[4]], top_region_plot_list[[5]], top_region_plot_list[[6]],
                  top_region_plot_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_",
                                          previous_CEDS_version, " - Top Emitting Regions" ) )
  } else {
    grid.arrange( top_region_plot_list[[1]], top_region_plot_list[[2]], top_region_plot_list[[3]],
                  top_region_plot_list[[4]], top_region_plot_list[[5]], top_region_plot_list[[6]],
                  top_region_plot_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( top_region_plot_list_dfs, file = paste0( "CEDS_version_comparison-CMIP_regions-",
                                                       CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Aggregate regions
  legend <- g_legend( agg_region_plot_list[[1]] )
  agg_region_plot_list <- lapply( agg_region_plot_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Aggregate_regions-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special', onefile = FALSE )
  library( "grid" )
  blank <- grid.rect( gp = gpar( col = "white" ) )

  if( include_titles_on_graphs ){
    grid.arrange( agg_region_plot_list[[1]], agg_region_plot_list[[2]], agg_region_plot_list[[3]],
                  agg_region_plot_list[[4]], agg_region_plot_list[[5]], agg_region_plot_list[[6]],
                  agg_region_plot_list[[7]], blank, legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_", previous_CEDS_version, " - Aggregate Regions" ) )
  }else{
    grid.arrange( agg_region_plot_list[[1]], agg_region_plot_list[[2]], agg_region_plot_list[[3]],
                  agg_region_plot_list[[4]], agg_region_plot_list[[5]], agg_region_plot_list[[6]],
                  agg_region_plot_list[[7]], blank, legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( agg_region_plot_list_dfs, file = paste0( "CEDS_version_comparison-Aggregate_regions-",
                                                       CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Africa - region by sector plot
  legend <- g_legend( africa_by_sector_list[[1]] )
  africa_by_sector_list <- lapply( africa_by_sector_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Africa_by_sec-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special' )

  if( include_titles_on_graphs ){
    grid.arrange( africa_by_sector_list[[1]], africa_by_sector_list[[2]], africa_by_sector_list[[3]],
                  africa_by_sector_list[[4]], africa_by_sector_list[[5]], africa_by_sector_list[[6]],
                  africa_by_sector_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_",
                                          previous_CEDS_version, " - Africa by sector" ) )

  } else {
    grid.arrange( africa_by_sector_list[[1]], africa_by_sector_list[[2]], africa_by_sector_list[[3]],
                  africa_by_sector_list[[4]], africa_by_sector_list[[5]], africa_by_sector_list[[6]],
                  africa_by_sector_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( africa_by_sector_df, file = paste0( "CEDS_version_comparison-Africa_by_sec-",
                                                  CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Region 1 - region by sector plot
  RCP_reg1_reg_by_sec <- gsub( "\\+", "", RCP_reg1_reg_by_sec ) # Some RCP regions have + in their names, remove
  RCP_reg1_reg_by_sec <- gsub( " ", "_", RCP_reg1_reg_by_sec )  # Some RCP regions have spaces in their names, replace with underscores

  legend <- g_legend( reg1_by_sector_list[[1]] )
  reg1_by_sector_list <- lapply( reg1_by_sector_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-', RCP_reg1_reg_by_sec, '_by_sec-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special' )

  if( include_titles_on_graphs ){
    grid.arrange( reg1_by_sector_list[[1]], reg1_by_sector_list[[2]], reg1_by_sector_list[[3]],
                  reg1_by_sector_list[[4]], reg1_by_sector_list[[5]], reg1_by_sector_list[[6]],
                  reg1_by_sector_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_",
                                          previous_CEDS_version, " - ", RCP_reg1_reg_by_sec, " by sector" ) )
  } else {
    grid.arrange( reg1_by_sector_list[[1]], reg1_by_sector_list[[2]], reg1_by_sector_list[[3]],
                  reg1_by_sector_list[[4]], reg1_by_sector_list[[5]], reg1_by_sector_list[[6]],
                  reg1_by_sector_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( reg1_by_sector_df, file = paste0( "CEDS_version_comparison-", RCP_reg1_reg_by_sec, "-",
                                                CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Region 2 - region by sector plot
  if( length( RCP_regions_for_reg_by_sec_comparison ) == 2 ){

    RCP_reg2_reg_by_sec <- gsub( "\\+", "", RCP_reg2_reg_by_sec ) # Some RCP regions have + in their names, remove
    RCP_reg2_reg_by_sec <- gsub( " ", "_", RCP_reg2_reg_by_sec )  # Some RCP regions have spaces in their names, replace with underscores

    legend <- g_legend( reg2_by_sector_list[[1]] )
    reg2_by_sector_list <- lapply( reg2_by_sector_list, function( x ) x + theme( legend.position = "none" ) )
    pdf( paste0( 'CEDS_version_comparison-', RCP_reg2_reg_by_sec, '_by_sec-', CEDS_start_year, "_", CEDS_end_year,
                 '.pdf' ), width = 12, height = 10, paper ='special' )

    if( include_titles_on_graphs ){
      grid.arrange( reg2_by_sector_list[[1]], reg2_by_sector_list[[2]], reg2_by_sector_list[[3]],
                    reg2_by_sector_list[[4]], reg2_by_sector_list[[5]], reg2_by_sector_list[[6]],
                    reg2_by_sector_list[[7]], legend, ncol = 4,
                    top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_",
                                            previous_CEDS_version, " - ", RCP_reg2_reg_by_sec, " by sector" ) )
    } else {
      grid.arrange( reg2_by_sector_list[[1]], reg2_by_sector_list[[2]], reg2_by_sector_list[[3]],
                    reg2_by_sector_list[[4]], reg2_by_sector_list[[5]], reg2_by_sector_list[[6]],
                    reg2_by_sector_list[[7]], legend, ncol = 4 )
    }

    dev.off( )

    write.xlsx( reg2_by_sector_df, file = paste0( "CEDS_version_comparison-", RCP_reg2_reg_by_sec, "-",
                                                  CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )
  }

# ROW - region by sector plot
  legend <- g_legend( ROW_by_sector_list[[1]] )
  ROW_by_sector_list <- lapply( ROW_by_sector_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-ROW_by_sec-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special' )

  if( include_titles_on_graphs ){
    grid.arrange( ROW_by_sector_list[[1]], ROW_by_sector_list[[2]], ROW_by_sector_list[[3]],
                  ROW_by_sector_list[[4]], ROW_by_sector_list[[5]], ROW_by_sector_list[[6]],
                  ROW_by_sector_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_",
                                          previous_CEDS_version, " - ROW by sector" ) )
  } else {
    grid.arrange( ROW_by_sector_list[[1]], ROW_by_sector_list[[2]], ROW_by_sector_list[[3]],
                  ROW_by_sector_list[[4]], ROW_by_sector_list[[5]], ROW_by_sector_list[[6]],
                  ROW_by_sector_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( ROW_by_sector_df, file = paste0( "CEDS_version_comparison-ROW_by_sec-",
                                               CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Global by agg. sector
# TODO: This legend is very tall, and the bottom touches the edge of the pdf. Perhaps this legend could be split in 2
#       (one portion for the sectors, another portion for the CEDS versions).
  legend <- g_legend( global_sector_plot_list[[1]] )
  global_sector_plot_list <- lapply( global_sector_plot_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Global_by_CMIP_sectors-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special' )

  if( include_titles_on_graphs ){
    grid.arrange( global_sector_plot_list[[1]], global_sector_plot_list[[2]], global_sector_plot_list[[3]],
                  global_sector_plot_list[[4]], global_sector_plot_list[[5]], global_sector_plot_list[[6]],
                  global_sector_plot_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_", previous_CEDS_version, " - Global Emissions by Sector" ) )
  }else{
    grid.arrange( global_sector_plot_list[[1]], global_sector_plot_list[[2]], global_sector_plot_list[[3]],
                  global_sector_plot_list[[4]], global_sector_plot_list[[5]], global_sector_plot_list[[6]],
                  global_sector_plot_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( global_sector_plot_list_dfs, file = paste0( "CEDS_version_comparison-Global_by_CMIP_sectors-",
                                                          CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Global Total
  legend <- g_legend( global_total_plot_list[[1]] )
  global_total_plot_list <- lapply( global_total_plot_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Global_total-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper = 'special' )

  if( include_titles_on_graphs ){
    grid.arrange( global_total_plot_list[[1]], global_total_plot_list[[2]], global_total_plot_list[[3]],
                  global_total_plot_list[[4]], global_total_plot_list[[5]], global_total_plot_list[[6]],
                  global_total_plot_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_", previous_CEDS_version, " - Total Global Emissions" ) )
  }else{
    grid.arrange( global_total_plot_list[[1]], global_total_plot_list[[2]], global_total_plot_list[[3]],
                  global_total_plot_list[[4]], global_total_plot_list[[5]], global_total_plot_list[[6]],
                  global_total_plot_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( global_total_plot_list_dfs, file = paste0( "CEDS_version_comparison-Global_total-",
                                                         CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

# Global Total by Fuel
if( load_previous_run | previous_CEDS_version != "v2016_07_26" ){

  legend <- g_legend( global_fuel_plot_list[[1]] )
  global_fuel_plot_list <- lapply( global_fuel_plot_list, function( x ) x + theme( legend.position = "none" ) )
  pdf( paste0( 'CEDS_version_comparison-Global_total_by_fuel-', CEDS_start_year, "_", CEDS_end_year,
               '.pdf' ), width = 12, height = 10, paper ='special' )

  if( include_titles_on_graphs ){
    grid.arrange( global_fuel_plot_list[[1]], global_fuel_plot_list[[2]], global_fuel_plot_list[[3]],
                  global_fuel_plot_list[[4]], global_fuel_plot_list[[5]], global_fuel_plot_list[[6]],
                  global_fuel_plot_list[[7]], legend, ncol = 4,
                  top = paste0( "CEDS_", current_CEDS_version, " vs. ", "CEDS_", previous_CEDS_version, " - Total Global Emissions by Fuel" ) )
  }else{
    grid.arrange( global_fuel_plot_list[[1]], global_fuel_plot_list[[2]], global_fuel_plot_list[[3]],
                  global_fuel_plot_list[[4]], global_fuel_plot_list[[5]], global_fuel_plot_list[[6]],
                  global_fuel_plot_list[[7]], legend, ncol = 4 )
  }

  dev.off( )

  write.xlsx( global_fuel_plot_list_dfs, file = paste0( "CEDS_version_comparison-Global_total_by_fuel-",
                                                        CEDS_start_year, "_", CEDS_end_year ,".xlsx" ) )

} else {

  warning( "Global emissions by fuel will not be compared to CEDS ", previous_CEDS_version,
           " as this release did not make public global emissions by fuel." )

}

# Reset working directory
setwd( paste0( "../../../../", CEDS_ROOT, "/input" ) )

# ---------------------------------------------------------------------------
# 12. End

logStop( )

