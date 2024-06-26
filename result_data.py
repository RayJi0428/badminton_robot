class ResultData:
    # 类属性
    class_attribute = "I am a class attribute"

    reply_text = None
    reply_emojiIds = None
    reply_image = None

    # 初始化方法（构造函数）
    def __init__(self, text=None, emojiIds=None, image=None):
        # 实例属性
        self.reply_text = text
        self.reply_emojiIds = emojiIds
        self.reply_image = image

    # 实例方法
    def instance_method(self):
        return f"Instance attribute value: {self.instance_attribute}"

    # 类方法
    @classmethod
    def class_method(cls):
        return f"Class attribute value: {cls.class_attribute}"

    # 静态方法
    @staticmethod
    def static_method():
        return "I am a static method"
