package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.Member;
import com.boj.santa.santaboj.domain.entity.UserFeedback;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class UserFeedbackRepositoryImpl implements UserFeedbackRepository{

    private final EntityManager entityManager;

    @Override
    @Transactional
    public UserFeedback saveUserFeedback(UserFeedback userFeedback) {
        entityManager.persist(userFeedback);
        return userFeedback;
    }

    @Override
    public Long getUserFeedbackCount(String targetModelName, Member member) {

        Long memberId = member.getId();

        List<Long> resultList = entityManager
                .createQuery("select count(u) from UserFeedback u where u.member.id =: id group by u.modelName", Long.class)
                .setParameter("id", memberId)
                .getResultList();

        if (resultList.size() == 0){
            return 0L;
        }
        return resultList.get(0);
    }
}
