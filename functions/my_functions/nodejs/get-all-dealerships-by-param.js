/**
 * Get all dealerships
 */
const Cloudant = require('@cloudant/cloudant');

async function main(params) {
    const state_check = "state" in params;
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    try {
        const dealerships_db = cloudant.use('dealerships')

        // Check if "state" parameter has been provided
        // If so, then query by "state"
        if (state_check && params.state != "") {
            const query = {
                selector: {
                    st: params.state
                }
            }

            const response = await dealerships_db.find(query);

            return response
        }

        // Else return all documents
        const doclist = await dealerships_db.list({ include_docs: true })

        // let records = [];

        // for (let i = 0; i < doclist.total_rows; i++) {
        //     records.push(doclist.rows[i].doc);
        // }

        // return { "dealerships": records };
        return doclist

    } catch (error) {
        return { error: error.message };
    }

}
