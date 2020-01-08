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
    YI_LIAO = 2  # 医疗
    DIAN_YUAN = 9  # 朝阳电源
    KE_JI = 4  # 科技
    KE_WEI = 5  # 科威
    ZHE_ZI = 6  # 科发
    BO_KE = 7  # 柏克
    JING_YI = 8  # 精一




class ApplyStatus:
    """申请类型"""
    NEW = 1    # 新建
    ALTER = 2    # 修改
    DELETE = 3    # 删除
    INVALID = 4    # 停用

    FINISHED = 0    # 申请完成

