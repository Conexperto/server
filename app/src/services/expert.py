from src.models import Auth, Expert

class ExpertService():

    def __init__(self):
        self.__auth = Auth()

    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

    def create_expert_profile(self, body):
        expert = Expert(user=body['user'],
                        headline=body['headline'],
                        about_expert=body['about_expert'],
                        rating_average=0,
                        rating_stars=[0, 0, 0, 0],
                        rating=0,
                        link_video=body['link_video'],
                        session_done=0,
                        teach=body['teach'],
                        methods=body['methods'],
                        plan=['plan'])
        expert.add()
        expert.save()

        return {
            'expert': expert
        }

    def update_expert(self, expert, body):
        _expert = expert['expert']

        _expert.serialize(body)
        _expert.save()

        return {
            'expert': expert
        }

    def delete_expert(self, expert):
        _expert = expert
        _expert.delete()

        return {
            'success': True
        }


