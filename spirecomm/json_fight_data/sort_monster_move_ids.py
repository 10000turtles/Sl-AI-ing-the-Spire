
with open(f"monster_move_ids","r") as f_read:
    # with open(f"monster_move_ids","w") as f_write:
    lines = f_read.readlines()
    print(lines)
    lines.sort()

    with open(f"monster_move_ids","w") as f_write:
        f_write.writelines(lines)
    
