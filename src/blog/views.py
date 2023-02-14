"""Define Views."""

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import (
    EmptyPage,
    PageNotAnInteger,
    Paginator)
from django.http import (
    Http404,
    HttpResponseRedirect)
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render)
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .choices import PostStatus
from .forms import CreateEditPostForm
from .models import Post


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ DESKTOP
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@cache_page(60 * 5)
def post_list(request):
    """List of the all Blog Posts."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Posts
    # -------------------------------------------------------------------------
    if request.user.is_staff:
        posts = Post.objects.filter(
            status__in=[
                PostStatus.VISIBLE,
                PostStatus.DRAFT,
            ]
        )
    else:
        posts = Post.objects.filter(
            status__in=[
                PostStatus.VISIBLE,
            ]
        )

    # -------------------------------------------------------------------------
    # --- Filter QuerySet by Tag ID
    # -------------------------------------------------------------------------
    tag_id = request.GET.get("tag", None)

    if tag_id:
        try:
            posts = posts.filter(
                tags__id=tag_id,
            ).distinct()
        except Exception as exc:
            print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

    # -------------------------------------------------------------------------
    # --- Slice the Post List
    # -------------------------------------------------------------------------
    posts = posts[:settings.MAX_POSTS_PER_QUERY]

    # -------------------------------------------------------------------------
    # --- Paginate QuerySet
    # -------------------------------------------------------------------------
    paginator = Paginator(posts, settings.MAX_POSTS_PER_PAGE)

    page = request.GET.get("page")

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # ---------------------------------------------------------------------
        # --- If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # ---------------------------------------------------------------------
        # --- If page is our of range (e.g. 9999), deliver last page of
        #     results.
        posts = paginator.page(paginator.num_pages)

    return render(
        request, "blog/post-list.html", {
            "posts":        posts,
            "page_total":   paginator.num_pages,
            "page_number":  posts.number,
        })


@staff_member_required
def post_create(request):
    """Create the Post."""
    # -------------------------------------------------------------------------
    # --- Prepare Form(s)
    # -------------------------------------------------------------------------
    form = CreateEditPostForm(
        request.POST or None, request.FILES or None,
        user=request.user)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()

            # -----------------------------------------------------------------
            # --- Render HTML Email Content
            if "post-draft" in request.POST:
                post.status = PostStatus.DRAFT
                # -------------------------------------------------------------
                # --- TODO: Send confirmation Email
            else:
                post.status = PostStatus.VISIBLE
                # -------------------------------------------------------------
                # --- TODO: Send confirmation Email

            post.save()

            # -----------------------------------------------------------------
            # --- Save the Log

            return redirect("post-list")

        # ---------------------------------------------------------------------
        # --- Failed to create the Post
        # --- Save the Log

    return render(
        request, "blog/post-create.html", {
            "form":     form,
        })


@cache_page(60 * 1)
def post_details(request, slug):
    """Post Details."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Post
    # -------------------------------------------------------------------------
    post = get_object_or_404(
        Post,
        slug=slug,
    )

    if post.is_closed:
        raise Http404

    # -------------------------------------------------------------------------
    # --- Increment Views Counter
    # -------------------------------------------------------------------------
    post.increase_views_count(request)

    return render(
        request, "blog/post-details.html", {
            "post":     post,
        })


@staff_member_required
def post_edit(request, slug):
    """Edit the Post."""
    # -------------------------------------------------------------------------
    # --- Retrieve Blog Post
    # -------------------------------------------------------------------------
    post = get_object_or_404(
        Post,
        slug=slug,
    )

    if post.is_closed:
        raise Http404

    form = CreateEditPostForm(
        request.POST or None, request.FILES or None,
        user=request.user, instance=post)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()

            # -----------------------------------------------------------------
            # --- TODO: Send confirmation Email

            # -----------------------------------------------------------------
            # --- Save the Log

            return HttpResponseRedirect(
                reverse("post-details", kwargs={
                    "slug":     post.slug,
                }))

        # ---------------------------------------------------------------------
        # --- Failed to save the Post
        # --- Save the Log

    return render(
        request, "blog/post-edit.html", {
            "form":     form,
            "post":     post,
        })
