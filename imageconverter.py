# ==========================================================
# Copyright (c) 2013 Forest Giant, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================

import glob
import os

from PIL import Image


class ImageConverter(object):
    whitelisted_extensions = {"jpg", "png", "jpeg"}
    percentages = {
        "ldpi": {
            "mdpi":  1.333,
            "hdpi":  2.0,
            "xhdpi": 2.666,
        },
        "mdpi": {
            "ldpi":  .75,
            "hdpi":  1.5,
            "xhdpi": 2.0,
        },
        "hdpi": {
            "ldpi":  .5,
            "mdpi":  .75,
            "xhdpi": 1.333,
        },
        "xhdpi": {
            "ldpi": .375,
            "mdpi": .5,
            "hdpi": .666,
        },
    }

    def __init__(self, directory, type):
        self.directory = directory
        self.type_ = type

    def convert(self):
        files = []

        for extension in self.whitelisted_extensions:
            path = os.path.join(self.directory, "*.%s" % extension)
            for file_ in glob.glob(path):
                files.append(file_)

        for file_ in files:
            if self.type_ == "ldpi":
                self.convert_to("mdpi", file_)
                self.convert_to("hdpi", file_)
                self.convert_to("xhdpi", file_)
            if self.type_ == "mdpi":
                self.convert_to("ldpi", file_)
                self.convert_to("hdpi", file_)
                self.convert_to("xhdpi", file_)
            if self.type_ == "hdpi":
                self.convert_to("ldpi", file_)
                self.convert_to("mdpi", file_)
                self.convert_to("xhdpi", file_)
            if self.type_ == "xhdpi":
                self.convert_to("ldpi", file_)
                self.convert_to("mdpi", file_)
                self.convert_to("hdpi", file_)

    def convert_to(self, new_type, file_):
        image = Image.open(file_)
        filename = file_.split(os.sep)[-1]
        width, height = image.size

        new_image = image.resize((
            max(int(self.percentages[self.type_][new_type] * width), 1),
            max(int(self.percentages[self.type_][new_type] * height), 1)
        ), Image.ANTIALIAS)

        new_directory = os.path.realpath(os.path.join(
            self.directory,
            "..",
            new_type,
        ))
        try:
            os.mkdir(new_directory)
        except OSError:
            pass

        new_image.save("%s" % os.path.join(new_directory, filename))
