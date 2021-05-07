require("dotenv").config({ path: "reverse_engineering/.env" });
const fs = require("fs");

const user = process.env.OCI_USER;
const fingerprint = process.env.OCI_FINGERPRINT;
const tenancy = process.env.OCI_TENANCY;
const region = process.env.OCI_REGION;
const compartmentId = process.env.COMPARTMENT_ID;


const os = require("oci-objectstorage");
const common = require("oci-common");

(async () => {
    try {
        const privateKey = fs.readFileSync(process.env.OCI_KEY_FILE);
        const provider = new common.SimpleAuthenticationDetailsProvider(tenancy, user, fingerprint, privateKey, passphrase, common.Region.SA_SAOPAULO_1);
        const cli = new os.ObjectStorageClient({ authenticationDetailsProvider: provider });
        cli.endpoint = "http://localhost:12000";

        const r = await cli.getNamespace({});
        const namespace = r.value;

        const bucketDetails = {
            name: "bucket_name",
            compartmentId: "compartment_id"
        };

        const createBucketResponse = await cli.createBucket({
            namespaceName: namespace,
            createBucketDetails: bucketDetails
        });

        // Create stream to upload
        const stats = fs.statSync(process.env.OCI_KEY_FILE);
        const nodeFsBlob = new os.NodeFSBlob(process.env.OCI_KEY_FILE, stats.size);
        const objectData = await nodeFsBlob.getData();

        const putObjectResponse = await cli.putObject({
            namespaceName: namespace,
            bucketName: "bucket_name",
            putObjectBody: objectData,
            objectName: "folder/key.pem",
            contentLength: stats.size
        });
    } catch (err) {
        console.error(err);
    }
})();