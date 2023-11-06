URL =  'https://sgp-search.io/api/v1/post'

#variables
country_name = "Brazil"
fields_to_show = [
    "alternate_name",
    "sample_id",
    "section_name",
	  "basin_type",
    "site_type",
    "country",
    "state_province",
    "coord_lat",
    "coord_long",
    "project_name",
    "nd", 
    "mo", 
    "v",
    "u",
    "p",
    "su",
    "toc",
    "fe_hr_fe_t",
    "interpreted_age",
    "tic",
    "del_13c_org",
    "del_13c_carb"
]


BODY = {
  "type": "samples",
  "filters": {
    "country": [
      country_name
    ]
  },
  "show": fields_to_show
}

