package com.boj.santa.santaboj.domain.entity;

import lombok.Getter;

import javax.persistence.*;
import java.util.List;

@Entity
@Getter
public class Member {
    @Id
    @Column(name="MEMBER_ID")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true, nullable = false)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String bojId;

    @OneToMany(mappedBy = "member")
    private List<UserFeedback> userFeedbackList;

    public static Member createMember(String username, String password, String bojId){
        Member member = new Member();
        member.username = username;
        member.password = password;
        member.bojId = bojId;
        return member;
    }
}
