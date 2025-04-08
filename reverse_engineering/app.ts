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

        // // Create a service client
        // const clientAdmin = new QueueAdminClient({ authenticationDetailsProvider: provider });
        // // clientAdmin.endpoint = 'http://localhost:12000';
        // // const queueTest = await clientAdmin.createQueue({
        // //     createQueueDetails: {
        // //         compartmentId: compartmentId,
        // //         displayName: 'queue-test',
        // //         visibilityInSeconds: 60,
        // //         retentionInSeconds: 3600
        // //     }
        // // });

        // // console.log('queueTest', queueTest);


        // queue.queue.retentionInSeconds;

        // const response = await clientAdmin.listQueues({ compartmentId: compartmentId, lifecycleState: 'ACTIVE' });

        // console.log('items', response.queueCollection.items);

        const client = new QueueClient({ authenticationDetailsProvider: provider }, {
            retryConfiguration: OciSdkDefaultRetryConfiguration
        });
        client.endpoint = 'http://localhost:12000';

        const queueId = 'ocid1.queue.oc1.sa-saopaulo-1.amaaaaaaepyaiqaa5hevtxw4qwcn74lidgaj4ogc56qo43zosyhn2pgy5vea';
        // const putMessage = await client.putMessages({
        //     queueId: queueId,
        //     putMessagesDetails: {
        //         messages: [{ content: 'meu_conteudo' }]
        //     }
        // });
        // console.log('putMessage', putMessage);
        // // putMessage {
        // //     putMessages: { messages: [ [Object] ] },
        // //     opcRequestId: '90748C906DCB-11EE-B12D-557D64907/AE6F70BBE4830841876979DB016F3253/EEC06A140AFA655D62D6BE0C796088CD'
        // //   }

        // console.log('putMessage', putMessage.putMessages.messages); // putMessage [ { id: 54043195530795490, expireAfter: '2023-10-19T15:32:36.698Z' } ] 24 hours after creation

        // const stats = await client.getStats({ queueId: queueId });
        // console.log('stats', stats);
        // // stats {
        // //     queueStats: {
        // //       queue: { visibleMessages: 3, inFlightMessages: 0, sizeInBytes: 36 },
        // //       dlq: { visibleMessages: 0, inFlightMessages: 0, sizeInBytes: 0 }
        // //     },
        // //     opcRequestId: 'F1E417706DCB-11EE-840D-5D57805A3/F152EFE702D4B7A1C4B7FAB22B56308F/AC43218A9CC1F04E2C7588D1F834F893'
        // //   }

        // const messages = await client.getMessages({ queueId: queueId, limit: 1 });
        // console.log('messages', messages);
        // // messages {
        // //     getMessages: { messages: [ [Object] ] },
        // //     opcRequestId: '22DC8F606DCC-11EE-889D-612D6B1E9/F79D182D1B5EF39F17166EF88A2809D0/4F7F5F3A8985ABB7C57FE35351B9870F'
        // //   }
        // console.log('messages', messages.getMessages.messages);
        // // messages [
        // //     {
        // //       id: 54043195530795460,
        // //       content: 'meu_conteudo',
        // //       receipt: 'AbJWn7bA-fgZAPD7CgUyKb7o9LBakWydf86uas63dsvW7qaiF1HQWgqa3v_e_ZfWEkfZVQQOpkPtTT1g4AleYcdyGbQfQameWwFs-n--83Bqz4WfSJN30IZg3SY-oHgFUCy0xBSufoaH7_bdtdZRcCCicH9nCC78g5JZoCHpGUboM0kv-QwjyD-RNqMiEd5yMtigAOC6lJItJFUjrCXd_CRmDVT28AQKnzlv3i6tJ3KPvGC9tGElr2PWh6RZRJWmMxiW6Diq-IADh61cCiZj-_2s1N2H7dykqCRatpZWKvEBAurLWu_TYHnge_3kPp3x43swR8E6BLBooHMxSItvPydtzqxwuCWLwmQS0l0',
        // //       deliveryCount: 1,
        // //       visibleAfter: '2023-10-18T15:37:38.283Z', // default value 30 seconds
        // //       expireAfter: '2023-10-19T15:32:14.587Z',
        // //       metadata: undefined
        // //     }
        // //   ]

        // const deleted = await client.deleteMessage({ queueId: queueId, messageReceipt: 'AbJWn7bA-fgZAPD7CgUyKb7o9LBakWydf86uas63dsvW7qaiF1HQWgqa3v_e_ZfWEkfZVQQOpkPtTT1g4AleYcdyGbQfQameWwFs-n--83Bqz4WfSJN30IZg3SY-oHgFUCy0xBSufoaH7_bdtdZRcCCicH9nCC78g5JZoCHpGUboM0kv-QwjyD-RNqMiEd5yMtigAOC6lJItJFUjrCXd_CRmDVT28AQKnzlv3i6tJ3KPvGC9tGElr2PWh6RZRJWmMxiW6Diq-IADh61cCiZj-_2s1N2H7dykqCRatpZWKvEBAurLWu_TYHnge_3kPp3x43swR8E6BLBooHMxSItvPydtzqxwuCWLwmQS0l0' });
        // console.log('deleted', deleted);
        // // deleted {
        // //     opcRequestId: '94F39A206DCD-11EE-9C72-D5C2AC67B/2B20F9DC559CF810B7856EE92355701E/ECB0BBF85E62F4B5AE7ED544D2072B3F'
        // //   }
        // // 409 if didn't find receipt

        // const updated = await client.updateMessage({
        //     queueId: queueId,
        //     messageReceipt: 'AdcxGxAGNo9LALFq14ceYVRJi1VoTSyRTiQLfFpFNtNBmp4G4ZodEGHJ_EXKboWCcwJw7rDlbrH4SxFUMio0N070Q_Z4jiZB3iBwBmerKIIfkMKnNIKSz8QTZpJHqoRa1drhvBWIAb7HjvBPZZti-3EvT87wIjuX0KlxizmwhPnIDXXIVXd9j-gwYOrZwcWWP4dyUfdQPgsuD3rgFJW_2wBwwQc6rLOdpqVBNIUYi4-wVagxlAza4VF0pG808QT26Xj-g5qt6DM2p1DNGBA1gjC2Ia8Erz_fr1fBpadHuUd7MxftDweNSkRj_M515BDFauJjouolWjIfQL3vkXw2CvNxZbqt3Uf5F-QZQZk',
        //     updateMessageDetails: {
        //         visibilityInSeconds: 666
        //     }
        // });
        // console.log('updated', updated);
        // // updated {
        // //     updatedMessage: { id: 54043195530795490, visibleAfter: '2023-10-18T16:00:54.874Z' },
        // //     opcRequestId: 'F7B6CE206DCD-11EE-A009-CF772D1F5/00C0DB1ECA86E68C0225079CDAB37DFA/519984818FD916B30C0C2C623A992059'
        // //   }

    } catch (error) {
        console.error(error);
    }
})();
