package com.boj.santa.santaboj.domain.repository;

import com.boj.santa.santaboj.domain.entity.Member;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import javax.transaction.Transactional;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class MemberRepositoryImpl implements MemberRepository{

    private final EntityManager entityManager;

    @Override
    @Transactional
    public Member save(Member member) {
        entityManager.persist(member);
        return member;
    }

    @Override
    public Member findById(Long id) {
        return entityManager.find(Member.class, id);
    }

    @Override
    public Member findByUsername(String username) {
        List<Member> members = entityManager
                .createQuery("SELECT m FROM Member m WHERE m.username=:username", Member.class)
                .setParameter("username", username)
                .getResultList();
        if (members.isEmpty()){
            return null;
        }
        return members.get(0);
    }
}
