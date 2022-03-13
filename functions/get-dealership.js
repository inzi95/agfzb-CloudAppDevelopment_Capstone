function main(params) {

    secret = {
        "iamApiKey": "dq4ca8I5OZmoM1Grn4HrIz2-RTUMIwepfgj57RM8fpJW",
        "url": "https://apikey-v2-9rn99dhfn3u2imxotbzqxwal0s2tpn46i3lb7wqim2f:d12bf06325b4f71100cba764082e9c08@2eea836a-90fd-4b86-8646-8cc9f19c0f91-bluemix.cloudantnosqldb.appdomain.cloud"
    }

    return new Promise(function (resolve, reject) {
        const Cloudant = require('@cloudant/cloudant');
        const cloudant = Cloudant({
            url: secret.url,
            plugins: { iamauth: { iamApiKey: secret.iamApiKey } }
        });
        const db_name = cloudant.use('dealerships');

        if (params.state) {

            db_name.find({
                "selector": {
                    "st": {
                        "$eq": params.state
                    }
                }
            }, function (err, result) {

                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 20 ~ err", err)
                    reject(err);
                }

                let code = 200;
                if (result.docs.length == 0) {
                    code = 404;
                }

                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result
                });
            });

        } else if (params.id) {

            id = parseInt(params.dealerId)
            db_name.find({ selector: { id: parseInt(params.id) } }, function (err, result) {

                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 20 ~ err", err)
                    reject(err);
                }

                let code = 200;
                if (result.docs.length == 0) {
                    code = 404;
                }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    body: result
                });

            });

        } else {
            db_name.list({ include_docs: true }, function (err, result) {

                if (err) {
                    console.log("🚀 ~ file: index.js ~ line 35 ~ err", err)
                    reject(err);
                }
                resolve({
                    statusCode: 200,
                    headers: { 'Content-Type': 'application/json' },
                    body: result
                });

            });

        }

    });

} 