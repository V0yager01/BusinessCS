const API_BASE = '';

function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        throw new Error('Токен не найден. Пожалуйста, войдите в систему.');
    }
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
}

async function apiRequest(url, options = {}) {
    try {
        const headers = getAuthHeaders();
        const response = await fetch(url, {
            ...options,
            headers: { ...headers, ...options.headers }
        });
        
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = '/login';
            return;
        }
        
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Ошибка сервера' }));
            throw new Error(error.detail || `Ошибка: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

const UserAPI = {
    async getMe() {
        return apiRequest(`${API_BASE}/user/me`);
    },
    
    async register(data) {
        const response = await fetch(`${API_BASE}/user/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Ошибка регистрации' }));
            throw new Error(error.detail || 'Ошибка регистрации');
        }
        return await response.json();
    },
    
    async login(data) {
        const response = await fetch(`${API_BASE}/user/get_token`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Ошибка входа' }));
            throw new Error(error.detail || 'Ошибка входа');
        }
        const result = await response.json();
        localStorage.setItem('access_token', result.access_token);
        return result;
    },
    
    async deleteAccount() {
        return apiRequest(`${API_BASE}/user/remove`, { method: 'DELETE' });
    }
};

const TeamAPI = {
    async getMyTeams() {
        return apiRequest(`${API_BASE}/team/my`);
    },
    
    async getTeam(teamUuid) {
        return apiRequest(`${API_BASE}/team?team_uuid=${teamUuid}`);
    },
    
    async createTeam(data) {
        return apiRequest(`${API_BASE}/team`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async addUserToTeam(data) {
        return apiRequest(`${API_BASE}/team/user`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async removeUserFromTeam(teamUserUuid) {
        return apiRequest(`${API_BASE}/team/user?userteamuuid=${teamUserUuid}`, {
            method: 'DELETE'
        });
    },
    
    async updateUserRole(data) {
        return apiRequest(`${API_BASE}/team/user`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }
};

const TaskAPI = {
    async getMyTasks() {
        return apiRequest(`${API_BASE}/task/my`);
    },
    
    async getTeamTasks(teamUuid) {
        return apiRequest(`${API_BASE}/task/team/${teamUuid}`);
    },
    
    async getTask(taskUuid) {
        return apiRequest(`${API_BASE}/task?task_uuid=${taskUuid}`);
    },
    
    async createTask(data) {
        return apiRequest(`${API_BASE}/task`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async updateTask(taskUuid, data) {
        return apiRequest(`${API_BASE}/task/${taskUuid}`, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    },
    
    async deleteTask(taskUuid) {
        return apiRequest(`${API_BASE}/task?task_uuid=${taskUuid}`, {
            method: 'DELETE'
        });
    },
    
    async assignPerformer(taskUuid, performerUuid) {
        return apiRequest(`${API_BASE}/task/${taskUuid}/performer`, {
            method: 'PATCH',
            body: JSON.stringify({ performer: performerUuid })
        });
    },
    
    async changeStatus(taskUuid, status) {
        return apiRequest(`${API_BASE}/task/${taskUuid}/status`, {
            method: 'PATCH',
            body: JSON.stringify({ status })
        });
    },
    
    async addComment(taskUuid, text) {
        return apiRequest(`${API_BASE}/task/${taskUuid}/comment`, {
            method: 'POST',
            body: JSON.stringify({ text })
        });
    }
};

const MeetingAPI = {
    async getMyMeetings() {
        return apiRequest(`${API_BASE}/meeting/mymeetings`);
    },
    
    async createMeeting(data) {
        return apiRequest(`${API_BASE}/meeting`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    
    async inviteUsers(meetingUuid, userIds) {
        return apiRequest(`${API_BASE}/meeting/${meetingUuid}/invite`, {
            method: 'POST',
            body: JSON.stringify({ uuid: userIds })
        });
    },
    
    async deleteMeeting(meetingUuid) {
        return apiRequest(`${API_BASE}/meeting?meeting_uuid=${meetingUuid}`, {
            method: 'DELETE'
        });
    }
};

const EvaluationAPI = {
    async getMyEvaluations(startDate, endDate) {
        return apiRequest(`${API_BASE}/evaluation/me?star_date=${startDate}&end_date=${endDate}`);
    },
    
    async getMyAvgRate() {
        return apiRequest(`${API_BASE}/evaluation/me/avg`);
    },
    
    async rateTask(taskUuid, rate) {
        return apiRequest(`${API_BASE}/evaluation?task_uuid=${taskUuid}&rate=${rate}`, {
            method: 'POST'
        });
    }
};

