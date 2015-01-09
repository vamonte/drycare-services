#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.base import Base


class Device(Base):

    NAME = "device"

    @classmethod
    def queries(cls, limit, offset, filters):
        return cls.wrapper().queries(limit, offset, filters)

    @classmethod
    def save(cls, name, location, did):
        return cls.wrapper().save(name, location, did)

    @classmethod
    def update(cls, did, name=None, location=None):
        return cls.wrapper().update(did, name=name, location=location)

    @classmethod
    def get(cls, did):
        return cls.wrapper().get(did)

    @classmethod
    def remove(cls, did):
        return cls.wrapper().remove(did)
