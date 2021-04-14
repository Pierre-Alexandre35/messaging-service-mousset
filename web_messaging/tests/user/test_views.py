from time import sleep

from flask import url_for, json

from web_messaging.tests.session import ViewTestMixin, assert_status_with_message



class TestLogin(ViewTestMixin):
    def test_login_page(self):
        """ Login page renders successfully. """
        response = self.client.get(url_for('user.login'))
        assert response.status_code == 200
        
