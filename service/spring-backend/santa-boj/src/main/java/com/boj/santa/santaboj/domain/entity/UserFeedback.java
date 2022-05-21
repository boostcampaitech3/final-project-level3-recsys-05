package com.boj.santa.santaboj.domain.entity;

import lombok.Getter;

import javax.persistence.*;

@Entity
@Getter
public class UserFeedback {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="USER_FEEDBACK_ID")
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name="MEMBER_ID")
    private Member member;

    @Column
    private String modelName;

}
