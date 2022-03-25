/**
 * Get all dealerships
 */
const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    // Create a Cloudant client
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    try {
        // Get the car-dealership database
        const dealerships_db = cloudant.use('dealerships')

        // Check if "state" or "dealerId" parameters have been provided
        // If so, then query by parameter
        if ("state" in params && params.state != "") {
            const query = {
                selector: {
                    st: params.state
                }
            }

            const response = await dealerships_db.find(query);
            return response

        } else if ("dealerId" in params && params.dealerId != "") {
            const query = {
                selector: {
                    id: Number(params.dealerId)
                }
            }

            const response = await dealerships_db.find(query);
            return response
        }

        // Else return all documents
        const doclist = await dealerships_db.list({ include_docs: true })
        return doclist

    } catch (error) {
        return { error: error.message };
    }

}
