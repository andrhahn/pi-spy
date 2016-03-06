# pi-spy

Camera functions for Raspberry Pi

### Getting Started

##### Setup
    Install NodeJS
    Create Amazon S3 account
    
##### Commands
    Install: npm install grunt-cli -g && npm install bower -g && bower install && npm install
    Build: grunt build
    Deploy to S3: grunt deploy
    Run webserver: node server.js

### Environment variables
#### Grunt - build
    API_HOST: http://localhost:1337

#### Grunt - deploy
    API_HOST: <rest api server uri>
    S3_ACCESS_KEY_ID: <S3 account information>
    S3_SECRET_ACCESS_KEY: <S3 account information>
    S3_BUCKET_NAME: <S3 account information>

### License

[The MIT License](http://opensource.org/licenses/MIT)
