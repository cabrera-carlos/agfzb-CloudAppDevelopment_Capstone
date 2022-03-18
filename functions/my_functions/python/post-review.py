#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException


def main(dict):
    authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url(dict["COUCH_URL"])

    try:
        response = service.post_document(db='reviews', document=dict["review"]).get_result()

        return { "review": response}

    except ApiException as ae:
        print("Method failed")
        return {"status code" : str(ae.code), "error message": ae.message}
