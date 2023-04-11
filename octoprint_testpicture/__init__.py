import octoprint.plugin

from octoprint.schema.webcam import Webcam, WebcamCompatibility

import os

import flask


class TestPictureWebcamPlugin(
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.WebcamProviderPlugin,
):
    # ~~ TemplatePlugin API

    def get_template_configs(self):
        return [
            {
                "type": "webcam",
                "name": "Test Picture",
                "template": "testpicture_webcam.jinja2",
            }
        ]

    # ~~ WebcamProviderPlugin API

    def get_webcam_configurations(self):
        return [
            Webcam(
                name="testpicture",
                displayName="Test Picture",
                canSnapshot=True,
                snapshot="Internal Testimage",
                compat=WebcamCompatibility(
                    snapshot="/plugin/testpicture/static/testpicture.jpg",
                    stream="/plugin/testpicture/static/testpicture.jpg",
                ),
            )
        ]

    def take_webcam_snapshot(self, webcamName):
        return [
            self._get_snapshot(),
        ]

    # ~~ SoftwareUpdate hook

    def get_update_information(self):
        return dict(
            testpicture=dict(
                displayName=f"{self._plugin_name} Plugin",
                displayVersion=self._plugin_version,
                # version check: github repository
                type="github_release",
                user="OctoPrint",
                repo="OctoPrint-Testpicture",
                current=self._plugin_version,
                # update method: pip
                pip="https://github.com/OctoPrint/OctoPrint-Testpicture/archive/{target_version}.zip",
            )
        )

    # ~~ Helpers

    def _get_snapshot(self):
        path = os.path.join(os.path.dirname(__file__), "static", "testpicture.jpg")
        with open(path, "rb") as f:
            return f.read()


__plugin_name__ = "Test Picture Webcam"
__plugin_pythoncompat__ = ">=3.7,<4"
__plugin_implementation__ = TestPictureWebcamPlugin()
__plugin_hooks__ = {
    "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
}
