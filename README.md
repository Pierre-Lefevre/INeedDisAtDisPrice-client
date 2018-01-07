# INeedDisAtDisPrice

## Get started

Launch your MongoDB server from anywhere :

`> mongod`

### MERN application :

Move to the app/server directory :

`> cd app/server`

Install all dependencies :

`> npm install`

Move to the app/client directory :

`> cd ../client`

Install all dependencies :

`> npm install`

Open 3 command prompt.
First one, start MERN's server :

`> cd app/server`

`> node index.js`

Second, start Webpack :

`> cd app/client`

`> npm run start-w`

Third, start MERN's client :

`> cd app/client`

`> npm run start`

### Meteor application :

Move to the Meteor directory :

`> cd meteor`

Install all dependencies :

`> npm install`

Edit the "MONGO_URL" environment variable (or edit it directly and permanently in Windows):

`> set MONGO_ULR=mongodb://localhost:27017/iNeedDisAtDisPrice`

Launch Meteor project :

`> meteor`

Go to : http://localhost:3000/
