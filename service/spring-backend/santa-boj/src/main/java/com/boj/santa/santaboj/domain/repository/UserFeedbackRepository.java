package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.UserFeedback;

public interface UserFeedbackRepository {
    UserFeedback saveUserFeedback(UserFeedback userFeedback);
}
