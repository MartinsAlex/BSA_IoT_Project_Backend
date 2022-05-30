[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)    
[![Npm package license](https://badgen.net/npm/license/discord.js)]()

# BSA_IoT_Project_Backend

## Use in the project
This backend which is dockerized served the frontend to get values from different APIs. The following scheme explains the architecture of the entire system :

![archi](archi.svg)

## Files structure
- *Files folder* : Contains all HTML to convert to PNG and the resulting PNGs
- *Templates folder* : Contains all HTML pages of the service
- *main.py* : Is the executable file to launch the server
- *utils.py* : Conatins all used functions
  
## Keys management
API keys (OpenWeather and PSPDFKit) are registered as environment variables, 
as specified in the Dockerfile.
