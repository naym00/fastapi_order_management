from fastapi import status

class Generic:
    def g_u_d_single(self, data, response, details):
        flag = True
        if not data:
            flag = False
            response.status_code = status.HTTP_404_NOT_FOUND
            details.update({'error': {'code': 'not_found', 'message': 'The requested resource was not found'}})
        else: details.update({'data': data})
        return flag