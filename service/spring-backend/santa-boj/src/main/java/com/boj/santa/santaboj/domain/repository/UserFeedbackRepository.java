package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.entity.UserFeedback;

public interface UserFeedbackRepository {
    UserFeedback saveUserFeedback(UserFeedback userFeedback);
    Long getUserFeedbackCount(String targetModelName, Member member);
}
