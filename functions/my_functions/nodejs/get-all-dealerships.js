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
        const doclist = await dealerships_db.list({ include_docs: true })

        let records = [];

        for (let i = 0; i < doclist.total_rows; i++) {
            // console.log(doclist.rows[i].doc)
            records.push(doclist.rows[i].doc);
        }

        return { "dealerships": records };

    } catch (error) {
        return { error: error.message };
    }

}
