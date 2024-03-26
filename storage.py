from aiogram.dispatcher.storage import BaseStorage


class SQLAlchemyStorage(BaseStorage):
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def get_state(self, user):
        session = self.sessionmaker()
        state = session.query(State).filter_by(user_id=user).first()
        session.close()
        return state.state if state else None

    async def set_state(self, user, state):
        session = self.sessionmaker()
        state_obj = session.query(State).filter_by(user_id=user).first()
        if state_obj:
            state_obj.state = state
        else:
            session.add(State(user_id=user, state=state))
        session.commit()
        session.close()
