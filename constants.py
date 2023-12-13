URL =  'https://sgp-search.io/api/v1/post'

#variables
country_name = ["Antarctica","Atlantic","Argentina","Australia","Austria","Barents Sea","Belgium","Black Sea","Bolivia","Brazil","Caribbean Sea","Canada","Chile","China","Colombia","Denmark","Czech Republic","Egypt","Ethiopia","Estonia","Finland","Gabon","Ghana","Germany","France","Greenland","Guyana","Gulf of Mexico","Indian","India","Japan","Korea, South","Latvia","Jordan","Italy","Indonesia","Libya","Mauritania","Madagascar","Mexico","Mediterranean Sea","Morocco","New Caledonia","New Zealand","Namibia","Mongolia","North America","North Pacific","Oman","North Atlantic","Pacific","Norway","Pakistan","Poland","Red Sea","Russia","Senegal","South Africa","South Atlantic","South Pacific","Spain","Sri Lanka","Svalbard and Jan Mayen Islands","Sweden","Switzerland","Tanzania","Ukraine","United States","United Kingdom","Zimbabwe","Venezuela"]
fields_to_show = [  
    "toc",
    "fe_hr_fe_t",
    "interpreted_age",
    "os187_os188i",
]


BODY = {
  "type": "samples",
  "filters": {
    "country": 
      country_name
    
  },
  "show": fields_to_show
}

