create table if not exists aliases (
    id bigserial primary key,
    alias varchar(7) not null,
    source text not null,
    created_at timestamptz default now(),
    expire_at timestamptz default now() + interval '60 days'
);

create table if not exists clicks (
    id bigserial primary key,
    alias_id bigint not null references aliases(id),
    clicked_at timestamptz default now()
);