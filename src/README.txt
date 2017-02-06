Run using "python app.py" in the terminal within the src directory


Files:
  app.py - Creates the flask instance and loads the html pages
  config.py - Gets the config data from lost_config.json
  lost_config.json - Stores the config data

  index.html - Used as a test page
  login.html - Provides a login form to eventually verify a user
  logout.html - Shows the user they have logged out
  report_filter.html - Allows the user to specify the data they want to query
  facility_inventory_report.html - Shows the facility information
  in_transit_report.html - Shows the in transit information


Addendums:
  facility_inventory_report - Does not allow filtered querey by dates
  because current DB implementationdoes not have start dates or end dates for
  some of the inventory

  in_transit_report - Does not query do to missing data in my current
  db implementation
