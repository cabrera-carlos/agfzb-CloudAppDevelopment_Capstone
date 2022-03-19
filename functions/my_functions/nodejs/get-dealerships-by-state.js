/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });


    try {
        const dealerships_db = cloudant.use('dealerships')

        const query = {
            selector: {
                st: params.state
            }
        }

        const response = await dealerships_db.find(query);

        return { "dealerships": response.docs };

    } catch (error) {
        return { error: error.message };
    }

}
