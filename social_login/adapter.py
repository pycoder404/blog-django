from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field

from logs import logs


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        logs.info("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        user = super().populate_user(request, sociallogin, data)
        logs.info(" user id:{} and sociallogin.user:{}".format(id(user),id(sociallogin.user)))

        extra_data = sociallogin.account.extra_data
        source = sociallogin.account.provider
        logs.info("extra_data is:{} and type is:{}".format(extra_data, type(extra_data)))
        introduction = extra_data.get("bio")
        homepage = extra_data.get("html_url")
        avatar = extra_data.get('avatar_url')
        user_field(user, "introduction", introduction)
        user_field(user, "homepage", homepage)
        user_field(user, "avatar", avatar)
        user_field(user, 'source', source)
        logs.info("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        logs.info("user is:{} ".format(user))
        logs.info(" user id:{} and sociallogin.user:{}".format(id(user),id(sociallogin.user)))

        return user
