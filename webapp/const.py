class ProductStatus:
    """产品状态"""
    WAIT_SUBMIT = 1    # 待提交
    WAIT_PASS = 2    # 待审核
    PASS = 3    # 审核通过
    FAIL = 4    # 审核不通过


class AttributeType:
    """属性类型"""
    A = 1    # 属性
    C = 2    # 属性大类
    T = 3    # 属性小类


class Company:
    """公司"""
    GU_FEN = 1   # 股份
    JING_YI = 2  # 精一
    KE_WEI = 3   # 科威
    YI_LIAO = 4  # 医疗
    BO_KE = 5    # 柏克
    KE_JI = 6    # 科技
    ZHE_ZI = 7   # 浙子


class ApplyStatus:
    """申请类型"""
    NEW = 1    # 新建
    ALTER = 2    # 修改
    DELETE = 3    # 删除
    INVALID = 4    # 停用

    FINISHED = 0    # 申请完成

