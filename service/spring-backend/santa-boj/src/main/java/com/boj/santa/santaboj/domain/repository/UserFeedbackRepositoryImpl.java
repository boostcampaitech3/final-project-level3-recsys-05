package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.UserFeedback;
import lombok.RequiredArgsConstructor;

import javax.persistence.EntityManager;

@RequiredArgsConstructor
public class UserFeedbackRepositoryImpl implements UserFeedbackRepository{

    private final EntityManager entityManager;

    @Override
    public UserFeedback saveUserFeedback(UserFeedback userFeedback) {
        entityManager.persist(userFeedback);
        return userFeedback;
    }
}
