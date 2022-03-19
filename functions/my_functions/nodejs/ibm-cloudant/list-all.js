const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');


function main(params) {
    const apikey = "";
    const url = "";

    const authenticator = new IamAuthenticator({
        apikey: apikey
    });

    const service = new CloudantV1({
        authenticator: authenticator
    });

    service.setServiceUrl(url);


    service.getAllDbs()
        .then((response) => {
            // console.log(response.result);
            return { "dbs": response.result }
        })
        .catch(error => {
            if (error.code !== undefined && error.code === "ERR_INVALID_ARG_VALUE") {
                // The request was not sent, so there is no error status code, text and body
                console.log("Invalid argument value: \n" + error.message);
            } else {
                console.log("Error status code: " + error.status);
                console.log("Error status text: " + error.statusText);
                console.log("Error message:     " + error.message);
                console.log("Error details:     " + error.body)
            }
        });
}


console.log(main(""));
