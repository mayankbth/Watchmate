from rest_framework.throttling import UserRateThrottle
# this means i am adding restrictions only for logged in user. Because, these thing can not be done by logged out user
# or some anonymous user, like creating a review.


class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    # we define the restrictions for the scopes in "settings.py"
    # see this...
    # 'DEFAULT_THROTTLE_RATES': {
    #         'anon': '5/day', # Throttle Rate: one per day for non register user
    #         'user': '10/day'  # Throttle Rate: three per day for register user
    #     }


class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'

