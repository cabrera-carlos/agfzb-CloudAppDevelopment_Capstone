/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant/types');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });


    try {
        let dbList = await cloudant.db.list();
        return { "dbs": dbList };
    } catch (error) {
        return { error: error.description };
    }

}

params = {
    "COUCH_URL": "",
    "IAM_API_KEY": "",
    "COUCH_USERNAME": ""
}

const print = async () => {
    try {
        // await will prevent the execution of next line until this line is executed
        const result = await main(params);

        console.log(result)
    }
    catch (e) {
        console.log(e)
    }
}

print();
