# Lecture 7: Virtual Memory
- Each process sees its own virtual address space.
- The MMU translates virtual pages to physical frames using the page table.
- A TLB caches recent translations; a TLB miss requires a page table walk.
- Page fault: page not in memory -> OS loads it from disk (swap).
- Replacement policies: FIFO, LRU, Clock (second chance).
