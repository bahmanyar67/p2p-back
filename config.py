class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:test@localhost:3307/p2p_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY="26c8de6f5c87c1b4cc890c63b7bd08c1c7d0918024b767aeee3e57ecd57c02e8"