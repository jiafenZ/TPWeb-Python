# -*- coding: utf-8 -*-
# @Author : Jerry
# @Time : 2022/2/26 16:20

from Project.Case.Database.case_data_database import CaseData, CaseDataSchema
from Common.yaml_method import YamlMethod


class SprintCaseCount:
    """
    统计测试用例执行结果接口
    """

    @staticmethod
    def sprint_case_count(case_name_id):
        """
        统计测试用例执行结果接口
        :param case_name_id: 用例名称ID
        :return:
        """

        code = YamlMethod().read_data('code.yaml')['code']

        # 查询测试用例
        case_data = CaseData.query.filter_by(case_name_id=case_name_id).first()

        if case_data:
            case_schema = CaseDataSchema()
            data = case_schema.dump(case_data)

            case_text = data['text']
            # 统计用例总数
            total_case = case_text.count("'children': []")
            # 统计不执行用例数，不执行用例数不参与指标统计
            invalid_case = case_text.count("'progress': 4")
            # 统计有效用例总数
            valid_case = total_case - invalid_case
            # 统计执行通过用例数
            pass_case = case_text.count("'progress': 9")
            # 统计执行失败用例数
            fail_case = case_text.count("'progress': 1")
            # 统计执行阻塞用例数
            block_case = case_text.count("'progress': 5")
            # 统计已执行用例数(执行通过用例数+执行失败用例数+执行阻塞用例)
            executed_case = pass_case + fail_case + block_case
            if executed_case != 0:
                # 用例执行率
                executed_percent = "%.2f%%" % ((executed_case / valid_case) * 100)
                # 统计执行通过用例率
                pass_percent = "%.2f%%" % ((pass_case / executed_case) * 100)
                # 统计执行失败用例率
                fail_percent = "%.2f%%" % ((fail_case / executed_case) * 100)
                # 统计执行阻塞用例率
                block_percent = "%.2f%%" % ((block_case / executed_case) * 100)
            else:
                executed_percent = '0%'
                pass_percent = '0%'
                fail_percent = '0%'
                block_percent = '0%'

            # 依次将 有效用例总数、用例执行率、执行通过率、执行失败率、执行阻塞率 放入统计结果列表
            result_list = [valid_case, executed_percent, pass_percent, fail_percent, block_percent]
        else:
            result_list = ['未知', '未知', '未知', '未知', '未知']

        res = {
            'code': code[0],
            'message': 'success',
            'data': {
                'result': result_list
            }
        }

        return res
