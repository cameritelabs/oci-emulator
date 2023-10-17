import dotenv from 'dotenv';
dotenv.config();

import fs from "fs/promises";

const user = process.env.OCI_USER || '';
const fingerprint = process.env.OCI_FINGERPRINT || '';
const tenancy = process.env.OCI_TENANCY || '';
const region = process.env.OCI_REGION || '';
const compartmentId = process.env.COMPARTMENT_ID || '';
const passphare = process.env.OCI_PASS_PHRASE || '';
const ociKeyFile = process.env.OCI_KEY_FILE || '';

import { QueueAdminClient, QueueClient } from "oci-queue";
import { Region, SimpleAuthenticationDetailsProvider, OciSdkDefaultRetryConfiguration, NoRetryConfigurationDetails } from "oci-common";

(async () => {
    try {

        const privateKey = await fs.readFile(ociKeyFile);
        const provider = new SimpleAuthenticationDetailsProvider(tenancy, user, fingerprint, privateKey.toString(), passphare, Region.SA_SAOPAULO_1);

        // Create a service client
        const clientAdmin = new QueueAdminClient({ authenticationDetailsProvider: provider });
        clientAdmin.endpoint = 'http://localhost:12000';
        const queueTest = await clientAdmin.createQueue({
            createQueueDetails: {
                compartmentId: compartmentId,
                displayName: 'queue-test'
            }
        });
        console.log('queueTest', queueTest);

        const client = new QueueClient({ authenticationDetailsProvider: provider }, {
            retryConfiguration: NoRetryConfigurationDetails
        });

    } catch (error) {
        console.error(error);
    }
})();
