from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam
)
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, Cors

from .lambda_stack import LambdaStack
from .challenge_template_dynamo_table import TemplateDynamoTable


class TemplateStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.rest_api = RestApi(self, "ChallengeTemplateLeoGustavo_RestApi",
                                    rest_api_name="ChallengeTemplate_RestApi",
                                    description="This is the ChallengeTemplate RestApi",
                                    default_cors_preflight_options=
                                    {
                                        "allow_origins": Cors.ALL_ORIGINS,
                                        "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                                        "allow_headers": ["*"]
                                    },
                                )

        api_gateway_resource = self.rest_api.root.add_resource("mss-template", default_cors_preflight_options=
        {
            "allow_origins": Cors.ALL_ORIGINS,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": Cors.DEFAULT_HEADERS
        }
                                                               )

        self.dynamo_table = TemplateDynamoTable(self, "ChallengeTemplateLeoGustavoDynamoTable")

        ENVIRONMENT_VARIABLES = {
            "STAGE": "DEV",
            "DYNAMO_TABLE_NAME": self.dynamo_table.table.table_name,
            "DYNAMO_PARTITION_KEY": "PK",
            "DYNAMO_SORT_KEY": "SK",
            "REGION": self.region,
        }



        self.lambda_stack = LambdaStack(self, api_gateway_resource=api_gateway_resource,
                                        environment_variables=ENVIRONMENT_VARIABLES)

        ses_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                "ses:*",
            ],
            resources=[
                "*"
            ]
        )

        s3_admin_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=[
                "s3:*",
            ],
            resources=[
                "*"
            ]
        )

        for f in self.lambda_stack.functions_that_need_ses_permissions:
            f.add_to_role_policy(ses_admin_policy)

        for f in self.lambda_stack.functions_that_need_s3_permissions:
            f.add_to_role_policy(s3_admin_policy)



        