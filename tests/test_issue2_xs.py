#******************************************************************************************************
#  test_issue2_xs.py - Gbtc
#
#  Copyright © 2021, Grid Protection Alliance.  All Rights Reserved.
#
#  Licensed to the Grid Protection Alliance (GPA) under one or more contributor license agreements. See
#  the NOTICE file distributed with this work for additional information regarding copyright ownership.
#  The GPA licenses this file to you under the MIT License (MIT), the "License"; you may not use this
#  file except in compliance with the License. You may obtain a copy of the License at:
#
#      http://opensource.org/licenses/MIT
#
#  Unless agreed to in writing, the subject software distributed under the License is distributed on an
#  "AS-IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. Refer to the
#  License for the specific language governing permissions and limitations.
#
#******************************************************************************************************

import inspect
import os
from configparser import ConfigParser

from openHistorian.historianConnection import historianConnection
from openHistorian.phasorRecord import phasorRecord
from snapDB.snapClientDatabase import snapClientDatabase
from snapDB.snapConnection import snapConnection
from snapDB.treeStream import treeStream


REPO_ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")


def test_host_port_parses_without_indexerror():
    historian = historianConnection("localhost:38402")

    assert historian.hostAddress == "localhost"
    assert historian.port == 38402
    assert historian.HostAddress == "localhost:38402"


def test_host_port_custom_port_and_whitespace():
    historian = historianConnection(" 127.0.0.1 : 12345 ")

    assert historian.hostAddress == "127.0.0.1"
    assert historian.port == 12345


def test_bare_host_uses_default_port():
    historian = historianConnection("localhost")

    assert historian.hostAddress == "localhost"
    assert historian.port == snapConnection.DefaultPort
    assert historian.port == 38402


def test_basekv_returns_basekv_not_sourceindex():
    record = phasorRecord(
        id=10,
        deviceAcronym="TESTDEVICE",
        label="Voltage",
        type="V",
        phase="A",
        sourceIndex=1,
        baseKV=345,
    )

    assert record.BaseKV == 345
    assert record.SourceIndex == 1
    assert record.BaseKV != record.SourceIndex


def test_isdiposed_typo_removed():
    source = inspect.getsource(snapClientDatabase)

    assert "IsDiposed" not in source
    assert "self.reader.IsDisposed" in source
    assert hasattr(treeStream, "IsDisposed")
    assert not hasattr(treeStream, "IsDiposed")


def test_numpy_declared_in_install_requires():
    setup_cfg = os.path.join(REPO_ROOT, "setup.cfg")
    parser = ConfigParser()
    read = parser.read(setup_cfg)

    assert read, f"failed to read {setup_cfg}"
    requires = parser.get("options", "install_requires", fallback="")
    names = {line.strip().split()[0].split(">")[0].split("<")[0].split("=")[0].split("[")[0]
             for line in requires.splitlines() if line.strip()}

    assert "numpy" in names
