# -*- coding: utf-8 -*-
# @Author : Kevin
# @Time : 2022/3/28 11:41

from Common.mysql import db
from src.ApiTest.ApiInfo.Database.api_database import ApiInfo
from Common.yaml_method import YamlMethod
from sqlalchemy.exc import SQLAlchemyError


class DeleteApi:
    """
    删除基础接口
    """

    @staticmethod
    def delete_api(aip_id):
        """
        删除基础信息
        :param aip_id: 接口ID
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        info = ApiInfo.query.filter_by(id=aip_id).first()

        if info is not None:
            try:
                db.session.delete(info)
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                res = {
                    'code': code[5],
                    'data': [],
                    'message': '删除失败'
                }
                return res

            res = {
                'code': code[0],
                'data': [],
                'message': '删除成功'
            }
            return res

        else:
            res = {
                'code': code[3],
                'data': [],
                'message': '接口信息不存在'
            }
            return res
